
function getUserId() {

    const payload = JSON.parse(
        atob(token.split(".")[1])
    );

    return payload.user_id;
}

async function bookingoffer() {

    const response = await fetch("/api/bookings/booking/offer/",{
        headers:{
            "Content-type":"application/json",
            "Authorization": `Bearer ${token}`
        }

    })
    const data = await response.json();

    const offer = document.getElementById("offersTable");
    
    data.forEach(function (bookingoffers){
        let button = "";

        if (bookingoffers.status === "PENDING") {
            button = `
                <button onclick="accept(${bookingoffers.id})">
                    Accept
                </button>
            `;
        } 
        else if (bookingoffers.status === "ACCEPTED") {
            button = `
                <button onclick="complete(${bookingoffers.booking})">
                    Complete
                </button>
            `;
        }
        else if (bookingoffers.status === "COMPLETED") {
            button = `
            <button onclick="rating(${bookingoffers.booking})">
            rating
            </button>
            `;      
        }  
        else if (bookingoffers.status === "COMPLETED" ) {
            button = `
            <button onclick="rating(${bookingoffers.booking})">
            rating
            </button>
            `;      
        }          
   
        
        offer.innerHTML+=`
        <tr>
        <td>${bookingoffers.id}</td>
        <td>${bookingoffers.service_name}</td>
        <td>${bookingoffers.provider_name}</td>
        <td>${bookingoffers.provider_rating}</td>
        <td>${bookingoffers.price}</td>

        <td>${bookingoffers.status}</td>
        <td>${button}</td>
    
        </tr>
        `
    });

 
}
bookingoffer()

async function accept(id) {

    console.log("Offer ID:", id);

    const response = await fetch(
        `/api/bookings/booking/offer/accept/${id}`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            }
        }
    );

    const data = await response.json();

    console.log("Response Status:", response.status);
    console.log("Response Data:", data);

    if (response.ok) {
        window.location.href = "/booking_offers/";
    } else {
        alert(data.msg || "Unable to accept offer");
    }
}


async function complete(bookingId) {
    console.log("Booking ID:", bookingId);

    const response = await fetch(
        `/api/bookings/booking/${bookingId}/complete/`,
        {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            }
        }
    );

    const data = await response.json();

    console.log(data);

    if (response.ok) {
        window.location.href = "/booking_offers/";
    }
}
function rating(bookingid) {
    window.location.href = `/rating/${bookingid}`;
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
