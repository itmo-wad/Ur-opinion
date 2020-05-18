function AlertPass() {
    var password = document.getElementById("pass").value;
    var confirmPassword = document.getElementById("c_pass").value;
    if (password != confirmPassword) {
        alert("Passwords do not match.");
       
    }
}


// function to check empty or contains only spaces 
function check_spaces(str){
    if (!str.replace(/\s/g, '').length || str === "") {
        return true;
      }
return false;
};


function Validate() {
    var username = document.getElementById("username").value;
    var fullname = document.getElementById("fullname").value;
    var email = document.getElementById("email").value;
    var password = document.getElementById("pass").value;
    var confirmPassword = document.getElementById("c_pass").value;

    if (check_spaces(username) || check_spaces(email)  || check_spaces(password)  || check_spaces(confirmPassword)  || check_spaces(fullname) ) {
        alert("Fill all the fields");
        return false;
    }
    
    // if (username === "" || password === "" || password ==="" || confirmPassword==="" || fullname==="") {
    //     alert("Fill all the fields");
    //     return false;

    // }

    if (password != confirmPassword) {
        alert("Passwords do not match.");
        return false;       
    }

 
    return true;
}
