function show_ideas(ele) {
    str = ele.id;
    var taskid = str.substring(4, );
   

    var div_block_id = "div_"+taskid
    var dev_block = document.getElementById(div_block_id);

    dev_block.style.display = "block";
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

function hide_inpyt_new_idea(){
    var newidea = document.getElementById("newidea");
    var listideas = document.getElementById("listideas");

    if (newidea.style.display=="none"){
        newidea.style.display = "block";
listideas.style.height="60%"

    }
    else{
        newidea.style.display = "none";
        listideas.style.height="75%"

    }
}