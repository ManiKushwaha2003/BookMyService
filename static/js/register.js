const registerForm = document.getElementById("registerForm");
const messageBox = document.getElementById("messageBox");

registerForm.addEventListener("submit", register);

async function register(event) {
    event.preventDefault();

    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const phone = document.getElementById("phone").value;  
    const address = document.getElementById("address").value;  
    const role = document.getElementById("role").value;
    const password = document.getElementById("password").value;
    const confirm_pasword =document.getElementById("confirm_password").value;    

    if (username.trim() === ""){
        toastMessage("username is required")
        return;
    }

    if (email.trim() === ""){
        toastMessage("email is required")
        return;
    }

    if (phone.trim() === ""){
        toastMessage("phone no. is required")
        return;
    }    
    if (password.trim() === ""){
        toastMessage("password is required")
        return;
    }

    if (confirm_pasword.trim() === ""){
        toastMessage("password is required")
        return;
    }    

    if (password.trim().lenght <=8 ){
        toastMessage("password must be at least 8 character")
        return;
    }

    if (password !== confirm_pasword){
        toastMessage("pasword do not match")
        return;
    }
    if (address.trim() === ""){
        toastMessage("address is required")
        return;
    }




    const response = await fetch("/api/accounts/users/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: username,
            email: email,
            phone:phone,
            address:address,
            role: role,
            password: password,
            confirm_pasword:confirm_pasword,

        })
    });

    const data = await response.json();
    console.log("STATUS:", response.status);
    console.log("DATA:", data);
        
    if (response.ok) {

        messageBox.innerText = "Account created successfully";
        toastMessage("Account created successfully")
        setTimeout ( function(){
            window.location.href = "/accounts/user/login/";
        },5000);
    
   
    } else {

        messageBox.innerText = "Registration failed";
        console.log(data);
    }
}