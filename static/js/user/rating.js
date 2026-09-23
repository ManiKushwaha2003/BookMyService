

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
    document.getElementById("clientName").value = data.client_name
    document.getElementById("providerName").value = data.provider_name;
    document.getElementById("serviceName").value = data.service_name;
}

getdata();


async function provider_rating(event) {

    event.preventDefault();

    console.log("RATING FUNCTION CALLED");

    const bookingId = document.getElementById("bookingId").value;
    const ratingvalue = document.getElementById("rating").value;
    const comment = document.getElementById("comment").value;

    console.log("Booking:", bookingId);
    console.log("Rating:", ratingvalue);
    console.log("Comment:", comment);


    const response = await fetch(
        "/api/ratings/rating/",
        {
            method: "POST",

            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                booking: bookingId,
                rating: ratingvalue,
                comment: comment
            })
        }
    );

    const data = await response.json();

    console.log("POST DATA:", data);


    if (response.ok) {

        alert("Rating submitted successfully");

        window.location.href = "/user-dashboard/";

    } else {

        alert(data.msg || "Rating failed");
        window.location.href = "/booking_offers/";
    
        ;

    }
}


document.getElementById("ratingForm").addEventListener(
    "submit",
    provider_rating
);
