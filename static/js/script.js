window.onload = function () {
    var divtoload = $('#divtoload').text();
    var alertmsg = $('#alertmsg').text();
   
    if (divtoload == "loadteams") {
        $("#cards").load("/teams");

    }
    
    if (divtoload == "loadtasks") {
        $("#cards").load("/cards");

    }
    
    if (alertmsg != ""){
        alert(alertmsg);
    }

};



/* When the user clicks on the button, 
toggle between hiding and showing the dropdown content */
function showdrop() {
    document.getElementById("myDropdown").classList.toggle("show");
}

// Close the dropdown if the user clicks outside of it
window.onclick = function (event) {
    if (!event.target.matches('.dropbtn') && !event.target.matches('.loginlogo')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        var i;
        for (i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}