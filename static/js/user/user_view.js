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
    document.getElementById("userId").value = data.id;
    document.getElementById("username").value = data.username;
    document.getElementById("firstName").value = data.firstName;
    document.getElementById("lastName").value = data.lastname;
    document.getElementById("email").value = data.email;
    document.getElementById("phone").value = data.phone;
    document.getElementById("role").value = data.role;
    document.getElementById("address").value = data.address;
    document.getElementById("isActive").value = data.is_active;
    document.getElementById("isStaff").value = data.is_staff;
    document.getElementById("isSuperuser").value = data.is_superuser;
    document.getElementById("dateJoined").value = data.date_joined;
    document.getElementById("lastLogin").value = data.last_login;

}
getdata()