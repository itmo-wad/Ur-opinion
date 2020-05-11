function AlertPass() {
    var password = document.getElementById("pass").value;
    var confirmPassword = document.getElementById("c_pass").value;
    if (password != confirmPassword) {
        alert("Passwords do not match.");

    }
}


// function to check empty or contains only spaces 
function check_spaces(str) {
    if (!str.replace(/\s/g, '').length || str === "") {
        return true;
    }
    return false;
};


function validate_setting() {
    var fullname = document.getElementById("fullname").value;
    var email = document.getElementById("email").value;
    var password = document.getElementById("pass").value;
    var confirmPassword = document.getElementById("c_pass").value;

    if (check_spaces(email) || check_spaces(fullname)) {
        alert("Fill all the fields");
        return false;
    }

    if (password != confirmPassword) {
        alert("Passwords do not match.");
        return false;
    }

    var current_pass = prompt("Please your current password");
    document.getElementById("current_pass").value = current_pass

    if (current_pass == null) {
        return false;
    }

    return true;
}

function active_save() {

    document.getElementById("setting_submit").style.display = "block"

}