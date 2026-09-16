const loginForm = document.getElementById("loginForm");
const message = document.getElementById("message");

loginForm.addEventListener("submit", login);

async function login(event) {
    event.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    try {
        const response = await fetch("/api/accounts/token/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        });

        const data = await response.json();

        if (!response.ok) {
            message.innerText = "Login failed";
            message.style.color ="red"
            console.log(data);
            return;
        }

        localStorage.setItem("access", data.access);
        localStorage.setItem("refresh", data.refresh);

        const token = JSON.parse(atob(data.access.split(".")[1]));

        console.log("User ID:", token.user_id);

        const userResponse = await fetch(
            `/api/accounts/users/${token.user_id}/`,
            {
                headers: {
                    "Authorization": "Bearer " + data.access
                }
            }
        );

        const userData = await userResponse.json();

        console.log("User Data:", userData);
        console.log("Role:", userData.role);

        if (!userResponse.ok) {
            message.innerText = "User data not found";
            console.log(userData);
            return;
        }

        if (userData.role === "user") {
            window.location.href = "/user-dashboard/";
        } else if (userData.role === "provider") {
            window.location.href = "/provider-dashboard/";
    
        } else {
            message.innerText = "Invalid role";
        }

    } catch (error) {
        console.log(error);
        message.innerText = "Something went wrong";
    }
}