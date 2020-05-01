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



function show_new_team() {


    var dev_block = document.getElementById("preview_team");
    dev_block.style.display = "block";

    // remove additional input fields.
    // var last_chq_no = $('#total_chq').val();
    // while (last_chq_no > 1) {
    //     $('#mem_'+last_chq_no).remove();
    //     last_chq_no--;
    //     $('#total_chq').val(last_chq_no);
    //   }

};


function hide_new_team() {
    var test = document.getElementById("preview_team");
    test.style.display = "none";
};

// function add_input_field(){
//     var new_chq_no = parseInt($('#total_chq').val())+1;
//     var new_input="<input type='text' id='mem_"+new_chq_no+"' name='mem_"+new_chq_no+"' placeholder='Add Username for Team member'  autocomplete='off'>";
//     $('#new_chq').append(new_input);
//     $('#total_chq').val(new_chq_no)
//   }



//   function remove_input_field(){
//       var last_chq_no = $('#total_chq').val();

//       if(last_chq_no>1){
//         $('#mem_'+last_chq_no).remove();
//         $('#total_chq').val(last_chq_no-1);

//       }
//     }

function teams_add_mem() {
    var username = $('#mem_add').val();
    var members = $('#mem_list').val();
    if (username != "") {
        $('#mem_list').val(members + username + '\n');
        $('#mem_add').val("");
    }


};

function teams_clear_list() {

    $('#mem_list').val("");

};