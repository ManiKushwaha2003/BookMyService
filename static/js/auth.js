const publicPages = [
    "/",
    "/accounts/user/login/",
    "/accounts/user/register/",
    "/select-role/",
    "/accounts/google/callback",
];

const currentPath = window.location.pathname;

let token = localStorage.getItem("access");
let userData;

const isProtected = !publicPages.includes(currentPath);

if (!token && isProtected) {
    window.location.href = "/accounts/user/login/";
}

async function check() {

    token = localStorage.getItem("access");

    if (!token) {
        return;
    }

    try {

        const response = await fetch("/api/accounts/auth/me/", {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json"
            },
            credentials: "include"
        });

        const data = await response.json();

        console.log("data :,", data)

        if (data.error=="ROLE_NOT_SET") {
            window.location.href = "/select-role/"
        }

        console.log("ME API STATUS:", response.status);
        console.log("USER DATA:", data);

        if (response.status === 401) {

            localStorage.removeItem("access");
            localStorage.removeItem("refresh");

            if (isProtected) {
                window.location.href = "/accounts/user/login/";
            }

            return;
        }

        if (!response.ok) {
            return;
        }

        userData = data;

        if (userData.role == "user") {

            const Totalprovider =
                document.getElementById("totalproviderid");

            const Totaluser =
                document.getElementById("totaluserid");

            if (Totalprovider) {
                Totalprovider.style.display = "none";
            }

            if (Totaluser) {
                Totaluser.style.display = "none";
            }
        }

        if (userData.role == "admin") {

            const booking =
                document.getElementById("bookingid");

            if (booking) {
                booking.style.display = "none";
            }
        }

        if (userData.role == "user") {

            const service =
                document.getElementById("addservice");

            if (service) {
                service.style.display = "none";
            }
        }

        if (userData.role == "user") {

            const userlist =
                document.getElementById("userlist");

            if (userlist) {
                userlist.style.display = "none";
            }
        }

        if (typeof validatePermission === "function") {
            validatePermission();
        }

    } catch (error) {
        console.error("Auth error:", error);
    }
}

check();

function logout() {

    localStorage.removeItem("access");
    localStorage.removeItem("refresh");

    window.location.href = "/accounts/user/login/";
}

