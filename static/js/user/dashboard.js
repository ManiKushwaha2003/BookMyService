

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
    userData = data;
    document.getElementById("username").innerText = data.username;

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

        const response = await fetch("/api/bookings/booking/", {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        const bookings = await response.json();

        console.log("Bookings:", bookings);

        if (!response.ok) {
            console.log("Booking API Error:", bookings);
            return;
        }

        document.getElementById("totalBookings").innerText =
            bookings.length;

        const pendingBookings = bookings.filter(function(booking) {
            return booking.status === "PENDING";
        });

        const completedBookings = bookings.filter(function(booking) {
            return booking.status === "COMPLETED";
        });

        document.getElementById("pendingBookings").innerText =
            pendingBookings.length;

        document.getElementById("completedBookings").innerText =
            completedBookings.length;

        showBookings(bookings);

    } catch (error) {

        console.log("Booking Error:", error);

    }
}

function showBookings(bookings) {

    const table = document.getElementById("bookingTable");

    table.innerHTML = "";

    if (bookings.length === 0) {
        table.innerHTML = `
            <tr>
                <td colspan="3" class="text-center">
                    No bookings found
                </td>
            </tr>
        `;
        return;
    }

    bookings.forEach(function(booking) {

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
                        ${booking.service_name || "Service"}
                    </div>
                </td>

                <td>
                    ${booking.provider_name || "Not Assigned"}
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

async function gettotaluser() {

    const reponse = await fetch("/api/accounts/users/profile/",{

        headers:{
            "Authorization":`Bearer ${token}`
        }

    })
    const data = await reponse.json();
    const totaluser = data.filter(user => user.role === "user").length;
    document.getElementById("totaluser").textContent = totaluser;
}
gettotaluser()

async function gettotalprovider() {

    const reponse = await fetch("/api/accounts/provider/",{

        headers:{
            "Authorization":`Bearer ${token}`
        }

    })
    const data = await reponse.json();
    document.getElementById("totalprovider").innerText = data.length;
}
gettotalprovider()




function logout(){
    localStorage.removeItem("access")
    window.location.href="/accounts/user/login/"
};

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

