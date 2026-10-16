
function getUserId() {
    const payload = JSON.parse(atob(token.split(".")[1]));
    return payload.user_id;
}

async function getProviderData() {

    const userId = getUserId();

    const response = await fetch(
        `/api/accounts/users/${userId}/`,
        {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }
    );

    const data = await response.json();

    console.log("Provider Data:", data);

    document.getElementById("providerName").innerText = data.username;
}
getProviderData();
async function getRequests() {

    const response = await fetch(
        "/api/bookings/booking/provider/pending/",
        {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }
    );

    const data = await response.json();

    console.log("Pending Bookings:", data);

    const table = document.getElementById("requestsTable");

    table.innerHTML = "";

    document.getElementById("newRequests").innerText = data.length;

    data.forEach(function(booking) {

        table.innerHTML += `
            <tr>
                <td>${booking.client_name }</td>
                <td>${booking.service_name}</td>
         
                <td>${booking.status}</td>
                <td> 
            <button class="btn btn-info btn-sm"
                onclick="customerDetail(${booking.id})">
                Customer Detail
            </button>
                </td>
               
                <td>
                <button class="btn btn-primary btn-sm"
                    onclick="booking(${booking.id})">
                       Send Offer
                </button>
                </td>
            </tr>
        `;
    });
}

function customerDetail(bookingId) {
    window.location.href = `/customer-detail/${bookingId}/`;
}
function booking(bookingid) {
    window.location.href = `/provider-offer/${bookingid}/`;
}

getRequests();
async function getRating() {

    const response = await fetch(
        "/api/ratings/rating/",
        {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }
    );

    if (!response.ok) {
        return;
    }

    const data = await response.json();

    document.getElementById("providerRating").innerText =
        data.average_rating 
}
getRating();


async function complete() {

    const response = await fetch(
        "/api/bookings/provider/work/",
        {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }
    );

    const data = await response.json();

    console.log(" Bookings:", data);


    document.getElementById("completedJobs").innerText = data.length;
}
complete()

function logout(){
    localStorage.removeItem("access")
    window.location.href="/accounts/user/login/"
};

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