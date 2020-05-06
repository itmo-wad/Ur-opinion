window.onload = function () {
    var divtoload = $('#divtoload').text();
    var alertmsg = $('#alertmsg').text();
   
    if (divtoload == "loadteams") {
        $("#cards").load("/teams");

    }
    
    if (divtoload == "loadcreatedtasks") {
        $("#cards").load("/created");
        high_light_tab("btn_created_by_me");

    }

    if (divtoload == "shared") {
        $("#cards").load("/shared");
        high_light_tab("btn_shared_with_me");

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

//remove underline
function reset_heighlight_tab(tabid){
    var tab = document.getElementById(tabid);
    tab.style.textDecoration="none"
}
// highlight tab I'm in
function high_light_tab(tabid){
    reset_heighlight_tab("btn_in_progress");
    reset_heighlight_tab("btn_created_by_me");
    reset_heighlight_tab("btn_shared_with_me");
    reset_heighlight_tab("btn_archived");    

 //underline selected tab
    var tab = document.getElementById(tabid);
    tab.style.textDecoration="underline";

}