/* When the user clicks on the button, 
toggle between hiding and showing the dropdown content */
function myFunction() {
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

/* show adn hid div for new task and account setting
 */
function show_new_task(name, title, text) {

    var dev_block = document.getElementById("preview");
    dev_block.style.display = "block";



};


function hide_new_task() {
    var test = document.getElementById("preview");
    test.style.display = "none";
};



function show_new_team(name, title, text) {

    var dev_block = document.getElementById("preview_team");
    dev_block.style.display = "block";



};


function hide_new_team() {
    var test = document.getElementById("preview_team");
    test.style.display = "none";
};