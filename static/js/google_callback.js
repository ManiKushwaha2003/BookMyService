async function googlecallback() {

    const params = new URLSearchParams(window.location.search);
    const code = params.get("code");

    if (!code) {
        console.log("Google authorization code not found");
        return;
    }

    try {

        const response = await fetch(
            `/api/v1/auth/google/callback/?code=${encodeURIComponent(code)}`
        );

        const data = await response.json();

        console.log("Google callback response:", data);

        if (!response.ok) {
            console.log("Google login failed");
            return;
        }

        localStorage.setItem("access", data.access);
        localStorage.setItem("refresh", data.refresh);

        console.log("ACCESS SAVED:", localStorage.getItem("access"));
        console.log("ROLE:", data.role);

        if (data.role === "provider") {

            window.location.href = "/provider-dashboard/";
            return;
        }

        if (data.role === "user" || data.role === "admin") {

            window.location.href = "/user-dashboard/";
            return;
        }

        window.location.href = "/select-role/";

    } catch (error) {

        console.error("Google callback error:", error);
    }
}

googlecallback();