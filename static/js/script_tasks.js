/* show and hide div for new task  */
function show_new_task() {

    var dev_block = document.getElementById("preview");
    dev_block.style.display = "block";


    // var field = document.getElementById('datepublish');
    // var date = new Date();
    
    // // Set the date
    // field.value = date.getFullYear().toString() + '-' + (date.getMonth() + 1).toString().padStart(2, 0) + 
    //     '-' + date.getDate().toString().padStart(2, 0);

    //     alert(field.value);

    // set input date valur to today date
    document.getElementById("datepublish").valueAsDate = new Date()
};

function hide_new_task() {
    var test = document.getElementById("preview");
    test.style.display = "none";

};

// function to check empty or contains only spaces 
function check_spaces(str) {
    if (!str.replace(/\s/g, '').length || str === "") {
        return true;
    }
    return false;
};

// validate if no empty fileds when submeting new task
function Validate_new_task() {
    var name = $('#taskname').val();
    var desc = $('#taskdesc').val();
    var pub = $('#datepublish').val();
    var selecteam = $('#slc_teams option:selected').text();
    var eachperiod = $('#eachperiod').val();
    
    if (check_spaces(name) || check_spaces(desc) || check_spaces(pub) || check_spaces(eachperiod) || check_spaces(selecteam)) {
        alert("Fill all fields!!");
        return false;
    }

    return true;
};

function show_teams() {
    var test = document.getElementById("preview");
    test.style.display = "none";
    $("#cards").load("/teams");

};

