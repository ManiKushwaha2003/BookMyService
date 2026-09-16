
const token = localStorage.getItem("access");

const usergetapi = "/api/accounts/users/";
const serviecgetapi = "/api/services/service/";
const bookinggetapi = "/api/bookings/booking/";
const bookingviewapi = "/api/bookings/booking/1";


// user load
async function getuserbyid(){
    
    const payload = JSON.parse(atob(token.split(".")[1]));

    userID = payload.user_id;

    try{
        const response = await fetch(usergetapi+userID ,
            {

            headers:{
                    "Authorization": `Bearer ${token}`,
                    "Content-Type": "application/json"
            }
        });

        const data = await response.json();
        console.log(data)

       
    }
    catch(error){
        console.error("fail to fetch data ",error.mesage)

    }
}
getuserbyid()
// load service

async function serviceget() {
    try{

        const response = await fetch(serviecgetapi,{
            headers:{
                    "Authorization": `Bearer ${token}`,
                    "Content-Type": "application/json"
            }
        })
        const data = await response.json();

    }
    catch(error){
     console.log("error", error.message);
    }
    
}
serviceget()


//  booking list//
async function BookingGet() {

    const totalbookingElement = document.getElementById("totalBookings");

    try{

        const response = await fetch(bookinggetapi,{
            headers:{
                    "Authorization": `Bearer ${token}`,
                    "Content-Type": "application/json"
            }
        })
        const data = await response.json();
        if (totalbookingElement) {
           
            if (Array.isArray(data)) {
                totalbookingElement.textContent = data.length; 
            } 
        }

    }
    catch(error){
     console.log("error", error.message)
    }
    
}
BookingGet()

async function booking_detail() {

    const bookingTable = document.getElementById("bookingTable")

    try{
        const response = await fetch("",{
            headers:{
                    "Authorization": `Bearer ${token}`,
                    "Content-Type": "application/json"
            }

        })
        const data = await response.json();

       
    }
    catch(error){
        console.log("error",error.mesage)
    }
}



