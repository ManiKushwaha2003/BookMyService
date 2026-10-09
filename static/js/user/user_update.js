const userid = window.location.pathname.split("/")[2];
async function getdata() {

    const response = await fetch(
        `/api/accounts/users/${userid}`,
        {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }
    );

    const data = await response.json();
    document.getElementById("username").value = data.username;
    document.getElementById("email").value = data.email;
    document.getElementById("phone").value = data.phone;
    document.getElementById("role").value = data.role;
    document.getElementById("address").value = data.address;
    document.getElementById("is_active").value = data.is_active ? "true" : "false";

}
getdata()

async function updateuser(event) {
    try{
        event.preventDefault();
        const username = document.getElementById("username").value;
        const email = document.getElementById("email").value;
        const phone = document.getElementById("phone").value;
        const role = document.getElementById("role").value;
        const address = document.getElementById("address").value;
        const is_active = document.getElementById("is_active").value === "true";
        

        const response = await fetch (`/api/accounts/users/${userid}/`,{
            method: "PATCH",
            headers:{
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body:JSON.stringify({
                username:username,
                email:email,
                phone:phone,
                role:role,
                address:address,
                is_active:is_active
            })
        }
        );
        const data = await response.json();
        console.log(data)
        userData = data;

        if (response.ok){
            alert("Profile updated successfully");
            window.location.href = "/user-dashboard/";
        }
    }
    catch(error){
        console.log(error)
    }
    
}

function validatePermission() {

    if (userData.role !== "admin") {
        toastMessage("You don't have permission to access this page!");
 
        setTimeout(() => {
            localStorage.removeItem("access");
            window.location.href = "/accounts/user/login/";
        }, 1000);
 
        return;
    }
}