
async function  getdata() {

    const status = document.getElementById("statusFilter").value;
    const search = document.getElementById("search").value;


    const response = await fetch(`/api/bookings/provider/work/?status=${status}&search=${search}`,{
        headers:{
            "Authorization":`Bearer ${token}`
        }
    })
    const data = await response.json();
    console.log(data)

    const table = document.getElementById("completedWorkTable");
    table.innerHTML = "";

    data.forEach(function(complete){
        table.innerHTML+=`
        <tr>
        <td>${complete.id}</td>
        <td>${complete.client_name}</td>
        <td>${complete.service_name}</td>
        <td>${complete.price}</td>
        <td>${complete.status}</td>
        </tr>

        
        `
    })
    
}
getdata()
document.getElementById("statusFilter").addEventListener("change", function() {
    getdata();
});

document.getElementById("search").addEventListener("input", function() {
    getdata();
});

function validatePermission() {

    if (userData.role == "user" && isProtected) {
        alert("You don't have permission to access this page!");
 
        setTimeout(() => {
            localStorage.removeItem("access");
            window.location.href = "/accounts/user/login/";
        }, 1000);
 
        return;
    }
}
