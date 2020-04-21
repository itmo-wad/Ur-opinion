function AlertPass() {
    var password = document.getElementById("pass").value;
    var confirmPassword = document.getElementById("c_pass").value;
    if (password != confirmPassword) {
        alert("Passwords do not match.");
       
    }
}

function Validate() {
    var username = document.getElementById("username").value;
    var email = document.getElementById("email").value;
    var password = document.getElementById("pass").value;
    var confirmPassword = document.getElementById("c_pass").value;

    
    if (username === "" || email === "" || password ==="" || confirmPassword==="") {
        alert("You have to fill all the fields");
        return false;

    }

    if (password != confirmPassword) {
        alert("Passwords do not match.");
        return false;
       
    }

 
    return true;
}