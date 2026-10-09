
async function getdata() {
    
    const status = document.getElementById("statusFilter").value;
    const search = document.getElementById("search").value;
    const response = await fetch (`/api/bookings/booking/?status=${status}&search=${search}`,{
        headers:{
            "Authorization": `Bearer ${token}`
        }
    })
    const data = await response.json();
    console.log("data----",data)
    const table = document.getElementById("bookingsTable")
    table.innerHTML = "";

    data.forEach(function(booking){
        table.innerHTML+=`
        <tr>
        <td>${booking.id}</td>
        <td>${booking.service_name}</td>
        <td>${booking.provider_name}</td>
        <td>${booking.status}</td>
        </tr>

        `
    })

}
getdata()
document.getElementById("statusFilter").addEventListener("change", function() {
    getdata(); });
document.getElementById("search").addEventListener("input", function() {
    getdata();
});


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
