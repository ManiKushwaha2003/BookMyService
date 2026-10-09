function getUserId() {
    const payload = JSON.parse(atob(token.split(".")[1]));
    return payload.user_id;
}

async function getUserData() {
    try {
        const userId = getUserId();

        const response = await fetch(`/api/accounts/users/${userId}/`, {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        const data = await response.json();

        if (!response.ok) {
            return;
        }

        document.getElementById("username").value = data.username || "";
        document.getElementById("email").value = data.email || "";
        document.getElementById("phone").value = data.phone || "";
        document.getElementById("address").value = data.address || "";

    } catch (error) {
        console.log("User Error:", error);
    }
}

async function getProviderProfile() {
    try {
        const userId = getUserId();

        const response = await fetch(
            `/api/accounts/users/${userId}/provider-profile`,
            {
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            }
        );

        const data = await response.json();

        if (!response.ok) {
            return;
        }

        document.getElementById("description").value =
            data.description || "";

        data.services.forEach(id => {
            document.querySelector(
                `#services option[value="${id}"]`
            ).selected = true;
        });

    } catch (error) {
        console.log("Provider Error:", error);
    }
}

async function getServices() {
    try {
        const response = await fetch("/api/services/service/", {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        const data = await response.json();

        if (!response.ok) {
            return;
        }

        const serviceSelect = document.getElementById("services");

        serviceSelect.innerHTML = "";

        data.forEach(service => {
            const option = document.createElement("option");

            option.value = service.id;
            option.textContent = service.name;

            serviceSelect.appendChild(option);
        });

        getProviderProfile();

    } catch (error) {
        console.log("Service Error:", error);
    }
}

async function updateProfile(event) {
    event.preventDefault();

    const userId = getUserId();

    const services = [];

    const selected = document.getElementById("services").selectedOptions;

    for (let option of selected) {
        services.push(Number(option.value));
    }

    await fetch(`/api/accounts/users/${userId}/`, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({
            email: document.getElementById("email").value,
            phone: document.getElementById("phone").value,
            address: document.getElementById("address").value
        })
    });

    const response = await fetch(
        `/api/accounts/users/${userId}/provider-profile`,
        {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({
                services: services,
                description: document.getElementById("description").value
            })
        }
    );

    if (response.ok) {
        alert("Profile updated successfully");
        window.location.href = "/provider-dashboard/";
    }
}

document
    .getElementById("providerProfileForm")
    .addEventListener("submit", updateProfile);

getUserData();
getServices();
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
