async function  userlist() {
    const search = document.getElementById("search").value;
    const response = await fetch(`/api/accounts/users/profile/?search=${search}`,{
        headers:{
            "Authorization":`Bearer ${token}`
        }
    })
    const data = await response.json();
    const table = document.getElementById("usersTable")
    table.innerHTML = "";
    data.forEach(function(userlist){
        table.innerHTML+=`
        <tr>
        <td>${userlist.id}</td>
        <td>${userlist.username}</td>
        <td>${userlist.email}</td>
        <td>${userlist.role}</td>
        <td>${userlist.is_active}</td>
        <td>${userlist.phone}</td>

        <td>
            <button class="btn btn-primary btn-sm"
                onclick="update(${userlist.id})">
                    update
            </button>
            <button class="btn btn-secondary btn-sm"
                onclick="view(${userlist.id})">
                    view
            </button>
            <button class="btn btn-danger btn-sm"
                onclick="deleteuser(${userlist.id})">
                    delete
            </button>                        
        </td>

        </tr>
        `
    })

}
userlist()


document.getElementById("search").addEventListener("input", function() {
    userlist();
});
function update(id){
    window.location.href = `/user-update/${id}`
}

function view(id){
    window.location.href = `/user-view/${id}`
}

async function deleteuser(id){
    if (!confirm("Are you sure you want to delete this user?")) {
        return;
    }

    const response = await fetch (`/api/accounts/users/${id}/`,{
        method:"DELETE",
        headers:{
            "Authorization":`Bearer ${token}`
        }
    })

    if(response.ok){
        window.location.href="/user-dashboard/"
    }

}

function validatePermission() {

    if (userData.role !== "admin") {
        toastMessage("You don't have permission to access this page!");
 
        setTimeout(() => {
            localStorage.removeItem("access");
            window.location.href = "/accounts/user/login/";
        }, 1000);
 
        return;
    }
}
     
