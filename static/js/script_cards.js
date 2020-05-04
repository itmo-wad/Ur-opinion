function show_ideas() {
    var dev_block = document.getElementById("preview_ideas");
    dev_block.style.display = "block";

};

function hide_ideas() {

    var test = document.getElementById("preview_ideas");
    test.style.display = "none";
};

function Validate_new_idea(){
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