const LoginForm = document.getElementById("loginbank");


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





LoginForm.addEventListener("submit", async function (e) {
    e.preventDefault();

    const loginbtn = document.getElementById("signin-button");
    const d_data = new FormData(LoginForm);
    console.log(d_data);
    setLoading(loginbtn);
    try {
        const response = await fetch("/loginp", {
            method: "POST",
            body: d_data
        });

        const data = await response.json();

        clearLoading(loginbtn);

        if (data.status === "success") {
            window.location.href = "/verify";
            
        } else {
            alert(data.message || "Login failed");
        }

    } catch (error) {
        clearLoading(loginbtn);
        console.error("Error:", error);
        alert("An error occurred during Login");
    }
});