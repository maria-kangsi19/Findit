
function checkpswd(){
const pswd=document.querySelector("#pswd");
const confirm=document.querySelector("#confirm");

if(pswd.value !=confirm.value){
    alert("Password Doesnot Match!");
    return false;
}
}

async function registerUser(event) {
    event.preventDefault();  

    const email = document.getElementById("email").value;
    const password = document.getElementById("pswd").value;

    const data = {
        name: "user",   
        email: email,
        password: password
    };

    const response = await fetch("http://127.0.0.1:8000/api/register/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    const result = await response.json();

    alert("Account Created ✅");
    window.location.href = "login.html";
}
