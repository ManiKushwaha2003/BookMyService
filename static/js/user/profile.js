
function getUserId() {

    const payload = JSON.parse(
        atob(token.split(".")[1])
    );

    return payload.user_id;
}

async function getUserData() {

    try {

        const userId = getUserId();

        console.log("User ID:", userId);

        const response = await fetch(
            `/api/accounts/users/${userId}/`,
            {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            } );

        const data = await response.json();

        console.log("User Data:", data);

        if (!response.ok) {
            return;
        }

        document.getElementById("username").value = data.username || "";
        document.getElementById("email").value = data.email || "";
        document.getElementById("phone").value = data.phone || "";
        document.getElementById("address").value = data.address || "";

    } catch (error) {

        console.log("User Error:", error);

    }
}

getUserData();


async function updateuser() {
    try{
        const userId = getUserId();

        const username = document.getElementById("username").value;
        const email = document.getElementById("email").value;
        const phone = document.getElementById("phone").value;
        const address = document.getElementById("address").value;
        

        const response = await fetch (`/api/accounts/users/${userId}/`,{
            method: "PATCH",
            headers:{
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body:JSON.stringify({
                username:username,
                email:email,
                phone:phone,
                address:address,
            })
        }
        );
        const data = await response.json();
        console.log(data)

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

    if (userData.role == "provider" && isProtected) {
        toastMessage("You don't have permission to access this page!");
 
        setTimeout(() => {
            localStorage.removeItem("access");
            window.location.href = "/accounts/user/login/";
        }, 1000);
 
        return;
    }
}
