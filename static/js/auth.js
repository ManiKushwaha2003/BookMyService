const token = localStorage.getItem("access");
const publicPages = [
    "/",
    "/accounts/user/login/",
    "/accounts/user/register/"
]
const currentPath = window.location.pathname;

const isProtected = !publicPages.includes(currentPath)

if(!token && isProtected){
    window.location.href="/accounts/user/login/"

}

async function check(){
    if (!token){
        window.location.href="/accounts/user/login/";
    }

    const response = await fetch("/api/accounts/auth/me/",{
        headers:{
            "Authorization":`Bearer ${token}`,
            "Content-Type": "application/json"
        }
    })
    if (response.status === 401 && isProtected ){
        localStorage.removeItem("access");

        window.location.href="/accounts/user/login/";
        return
    }
    if (response.ok){
        

        console.log("token is valid")
    }

}

check()