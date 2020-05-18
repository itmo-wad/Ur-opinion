
/* show and hide div for creating a new team  */
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
    $('#teamname').val("");
    $('#teamdesc').val("");
    $('#mem_add').val("");
    $('#mem_list').val("");
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

// function to check empty or contains only spaces 
function check_spaces(str) {
    if (!str.replace(/\s/g, '').length || str === "") {
        return true;
    }
    return false;
};


// validate if no empty fileds when submeting new team
function Validate_new_team() {
    var name = $('#teamname').val();
    var desc = $('#teamdesc').val();
    var members = $('#mem_list').val();
    if (check_spaces(name) || check_spaces(desc) || check_spaces(members)) {
        alert("Fill all fields!!");
        return false;
    }

    return true;
};

// add new member to the textarea
function teams_add_mem() {
    var currentusername = $('#divusername').text();
    var member = $('#mem_add').val();
    var members = $('#mem_list').val();
    
    if (currentusername == member){
        alert("Please don't add yourself to team members, you are the boss!!");
        $('#mem_add').val("");
        return false;
    }

    if (member != "" && member.indexOf(' ') == -1) {
        $('#mem_list').val(members + member + '\n');
        $('#mem_add').val("");
        return true;
    } else {
        alert("Check if the field empty or contains spaces");
        $('#mem_add').val("");
        return false;
    }

};

// clear members from textarea
function teams_clear_list() {

    $('#mem_list').val("");

};


function confirm_remove_team(){
    return confirm('Are you sure you want remove the Team and all its tasks?')
}


function hide_team(ele) {
    str = ele.id;
    var taskid = str.substring(6, );

    var div_block_id = "div_"+taskid
    var test = document.getElementById(div_block_id);
    test.style.display = "none";
};


function show_team(ele) {
    str = ele.id;
    var taskid = str.substring(4, );
   

    var div_block_id = "div_"+taskid
    var dev_block = document.getElementById(div_block_id);

    dev_block.style.display = "block";

    };