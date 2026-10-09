async function serviceadd() {

    const name = document.getElementById("name").value;
    const description =document.getElementById("description").value;

    const response = await fetch("/api/services/service/",{
        method:"POST",
        headers:{
            "Content-Type": "application/json",
            "Authorization":`Bearer ${token}`
        },
        body:JSON.stringify({
            name:name,
            description:description
        })

    })
    const data = response.json();

    if (response.ok){
        alert("service ADDED")
        window.location.href="/user-dashboard/"
    }

    
}



function validatePermission() {

    if (userData.role == "provider" && isProtected) {
        toastMessage("You don't have permission to access this page!");
 
        setTimeout(() => {
            localStorage.removeItem("access");
            window.location.href = "/accounts/user/login/";
        }, 1000);
 
        return;
    }
}