

function getUserId() {

const payload = JSON.parse(atob(token.split(".")[1]));

return payload.user_id;

}

async function getUserData() {

try {
    const userId = getUserId();
    const response = await fetch(
        `/api/accounts/users/${userId}/`,
        {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }
    );

    const data = await response.json();

    if (!response.ok) {
        return;
    }


} catch (error) {
    console.log("User Error:", error);
}
}

async function getServices() {
try {

    const response = await fetch("/api/services/service/",
        {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }
    );

    const services = await response.json();

    return services;

} catch (error) {

    console.log("Service Error:", error);
    return [];}
}



async function getProviders() {
try {

    const response = await fetch("/api/accounts/users/",
        {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }
    );

    const users = await response.json();
    return users;
} catch (error) {
    console.log("Provider Error:", error);
    return [];

}
}


async function getBookings() {

try {
    const response = await fetch(
        "/api/bookings/booking/",
        {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }
    );

    const bookings = await response.json();
    if (!response.ok) {

        console.log("Booking API Error:",bookings
        );
        return;
    }

    const userId = getUserId();

    const myBookings = bookings.filter(function(booking) {

        return Number(booking.client) === Number(userId);

    });


    console.log("My Bookings:", myBookings);

    document.getElementById(
        "totalBookings"
    ).innerText = myBookings.length;

    const pendingBookings = myBookings.filter(function(booking){
        return booking.status === "PENDING";
    });

    const completedBooking = myBookings.filter(function(booking){
        return booking.status === "COMPLETED"
    });

    document.getElementById("pendingBookings").innerText = pendingBookings.length;
    document.getElementById("completedBookings").innerText = completedBooking.length

    const services = await getServices();
    const providers = await getProviders();

    showBookings( myBookings,services,providers
    );

    await getOffersCount(myBookings);


} catch (error) {

    console.log("Booking Error:", error
    );

}


}


function showBookings(bookings,services,providers) {

const table = document.getElementById( "bookingTable" );

table.innerHTML = "";
if (bookings.length === 0) {
    table.innerHTML = `
        <tr>
            <td colspan="5" class="text-center">
                No bookings found
            </td>
        </tr>
    `;

    return;

}


bookings.slice(0, 5).forEach(function(booking) {

    const service = services.find(function(item) {

        return Number(item.id) === Number(
            booking.service
        );

    });

    let providerName = "";
    if (booking.provider) {

        const provider = providers.find(function(item) {

            return Number(item.id) === Number(
                booking.provider
            );

        });


        if (provider) {

            providerName =
                provider.username;

        }

    }


    let statusClass = "pending";
    if (booking.status === "ACCEPTED") {
        statusClass = "accepted";

    }
    if (booking.status === "IN_PROGRESS") {
        statusClass = "active";
    }
    if (booking.status === "COMPLETED") {

        statusClass = "completed";

    }
    if (booking.status === "REJECTED") {

        statusClass = "rejected";

    }
    table.innerHTML += `

        <tr>
            <td>
                <div class="service-name">
                    <div class="table-icon">
                        <i class="bi bi-tools"></i>
                    </div>
                    ${service ? service.name : "Service"}
                </div>
            </td>
            <td>
                ${booking.description || "-"}
            </td>
            <td>
                ${providerName}
            </td>
            <td>
                <span class="status-badge ${statusClass}">
                    ${booking.status}
                </span>
            </td>
            
        </tr>
    `;

});


}


document.addEventListener("DOMContentLoaded",
function() {
    getUserData();
    getBookings();
    
    document .getElementById("bookServiceBtn").addEventListener("click",
            function() {
                window.location.href ="/create-booking/";
            }
        ); 
}
);


function logout(){
    localStorage.removeItem("access")
    window.location.href="/accounts/user/login/"
};