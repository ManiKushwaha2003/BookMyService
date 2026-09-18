const token = localStorage.getItem("access");

if (!token) {
    window.location.href = "/accounts/user/login/";
}


function getUserId() {
    const payload = JSON.parse(atob(token.split(".")[1]));

    return payload.user_id;
}

async function getClientName() {

    const clientId = getUserId();
    try {

        const response = await fetch(
            `/api/accounts/users/${clientId}/`,
            {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            }
        );

        const data = await response.json();

        if (response.ok) {

            document.getElementById("client").value = data.username;

        }

    } catch (error) {

        console.log("Client Error:", error);

    }
}

async function loadServices() {

    try {

        const response = await fetch(
            "/api/services/service/",
            {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            }
        );

        const services = await response.json();

        const serviceSelect = document.getElementById("service");

        services.forEach(function(service) {

            serviceSelect.innerHTML += `
                <option value="${service.id}">
                    ${service.name}
                </option>
            `;

        });

    } catch (error) {

        console.log("Service Error:", error);

    }
}

const bookingform = document.getElementById("bookingForm")
    bookingform.addEventListener("submit", async function(event) {
        event.preventDefault();

        const service = document.getElementById("service").value;
        const description =document.getElementById("description").value;

        const message = document.getElementById("message");
        const clientId = getUserId();
        try {

            const response = await fetch(
                "/api/bookings/booking/",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${token}`
                    },

                    body: JSON.stringify({
                        client: clientId,
                        service: service,
                        description: description
                    })
                }
            );

            const data = await response.json();

            if (response.ok) {

                document.getElementById("bookingForm").reset();
                getClientName();

                setTimeout(function() {
                    window.location.href = "/user-dashboard/";
                }, 1500);

            } 

        } catch (error) {

            console.log(error);

        }

    });


getClientName();
loadServices();