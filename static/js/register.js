const registerForm = document.getElementById("registerForm");
const messageBox = document.getElementById("messageBox");

registerForm.addEventListener("submit", register);

async function register(event) {
    event.preventDefault();

    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const role = document.getElementById("role").value;

    const response = await fetch("/api/accounts/users/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: username,
            email: email,
            password: password,
            role: role
        })
    });

    const data = await response.json();

    if (response.ok) {

        messageBox.innerText = "Account created successfully";


        window.location.href = "/accounts/user/login/";
   

    } else {

        messageBox.innerText = "Registration failed";
        console.log(data);
    }
}