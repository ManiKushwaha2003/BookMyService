
const bookingId = window.location.pathname.split("/")[2];

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

    console.log("Status:", response.status);
    console.log("DATA:", data);

    if (!response.ok) {
        console.log("Error:", data);
        return;
    }

    document.getElementById("bookingId").value = data.id || "-----";
    document.getElementById("clientName").value = data.client_name || "-----";
    document.getElementById("serviceName").value = data.service_name || "-----";
    document.getElementById("description").value = data.description || "-----";
    document.getElementById("status").value = data.status || "-----";
    document.getElementById("phone").value = data.client_phone || "-----";
    document.getElementById("email").value = data.client_email || "-----";
    document.getElementById("address").value = data.client_address || "-----";
}

getdata();
