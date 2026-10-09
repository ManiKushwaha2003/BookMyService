
function getUserId() {

    const payload = JSON.parse(
        atob(token.split(".")[1])
    );

    return payload.user_id;
}
async function getdata() {
    const response = await fetch ("/api/bookings/booking/provider/pending/",{
        headers:{
            "Authorization": `Bearer ${token}`
        }
    })
    const data = await response.json();
    const table = document.getElementById("bookingTable")

    data.forEach(function(booking){
        let button = "";

        table.innerHTML+=`
        <tr>
        <td>${booking.id}</td>
        <td>${booking.client_name}</td>
        <td>${booking.service_name}</td>
        <td>${booking.description}</td>
        <td>${booking.status}</td>
        <td>
            <button class="btn btn-primary btn-sm"
                onclick="booking(${booking.id})">
                    Send Offer
            </button>
        </td>
   
        </tr>

        `
    })

}
getdata()

function booking(bookingid) {
    window.location.href = `/provider-offer/${bookingid}/`;
}
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
