
function getUserId() {

    const payload = JSON.parse(
        atob(token.split(".")[1])
    );

    return payload.user_id;
}
async function getdata() {
    const response = await fetch ("/api/bookings/booking/",{
        headers:{
            "Authorization": `Bearer ${token}`
        }
    })
    const data = await response.json();
    const table = document.getElementById("bookingsTable")

    data.forEach(function(booking){
        table.innerHTML+=`
        <tr>
        <td>${booking.id}</td>
        <td>${booking.service_name}</td>
        <td>${booking.provider_name}</td>
        <td>${booking.description}</td>
        <td>${booking.status}</td>
        </tr>

        `
    })

}
getdata()