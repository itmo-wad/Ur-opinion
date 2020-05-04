function show_ideas(ele) {
    var dev_block = document.getElementById("preview_ideas");
    dev_block.style.display = "block";

    var taskid = ele.id;
    document.getElementById("taskid").value=taskid;

};

function hide_ideas() {

    var test = document.getElementById("preview_ideas");
    test.style.display = "none";
};


function check_spaces(str) {
    if (!str.replace(/\s/g, '').length || str === "") {
        return true;
    }
    return false;
};


function Validate_new_idea(){
    var memidea = $('#memidea').val();

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
listideas.style.height="65%"

    }
    else{
        newidea.style.display = "none";
        listideas.style.height="75%"

    }
}