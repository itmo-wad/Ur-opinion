function show_ideas(ele) {
    str = ele.id;
    var taskid = str.substring(4, );
   

    var div_block_id = "div_"+taskid
    var dev_block = document.getElementById(div_block_id);

    dev_block.style.display = "block";


    // hide input and save button if he has the rights to add
    var input_status = "statusmem_"+taskid
    var status = document.getElementById(input_status).value;
  
    if (status == 0)  {
// hide the input
hide_input_idea_for_mem(taskid);
    }
    };

function hide_ideas(ele) {
    str = ele.id;
    var taskid = str.substring(6, );

    var div_block_id = "div_"+taskid
    var test = document.getElementById(div_block_id);
    test.style.display = "none";
};


function check_spaces(str) {
    if (!str.replace(/\s/g, '').length || str === "") {
        return true;
    }
    return false;
};


function Validate_new_idea(ele){
    str = ele.id;
    var taskid = str.substring(8, );

    textareid = "memidea_"+taskid
    var memidea = document.getElementById(textareid).value;

    if(check_spaces(memidea)){
        alert("Not allowed input !!");
        return false;
    }

    return true;
}

function hide_input_idea_for_mem(taskid){
    
    var textarea = "memidea_"+taskid
    document.getElementById(textarea).style.display="none";

    var save="ideabtn_"+taskid    
    document.getElementById(save).style.display="none";;

    var listideas = "listideas_" + taskid
    document.getElementById(listideas).style.height="75%";
   
}
