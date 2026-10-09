

const bookingId = window.location.pathname.split("/")[2];

console.log("Booking ID:", bookingId);


async function getdata() {

    const response = await fetch(
        `/api/bookings/booking/${bookingId}`,
        {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }
    );

    const data = await response.json();

    console.log("DATA:", data);

    if (!response.ok) {
        console.log("Error:", data);
        return;
    }
 
    document.getElementById("bookingId").value = data.id;
    document.getElementById("service").value = data.service_name;
}

getdata();


async function provider_offer(event) {

    event.preventDefault();

    const bookingId = document.getElementById("bookingId").value;
    const price = document.getElementById("price").value;
    const messages = document.getElementById("messages").value;


    console.log("Booking:", bookingId);


    const response = await fetch(
        "/api/bookings/booking/offer/",
        {
            method: "POST",

            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                booking: bookingId,
                price: price,
                messages: messages
            })
        }
    );

    const data = await response.json();

    console.log("POST DATA:", data);


    if (response.ok) {

        alert("submitted successfully");

        window.location.href = "/provider-dashboard/";

    } else {

        alert(data.msg || "Rating failed");
        window.location.href = "#";
    
        ;

    }
}

document.getElementById("offerForm").addEventListener(
    "submit",provider_offer
    
);
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

