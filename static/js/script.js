function scroll_to_cards() {
    $('html,body').animate({
      scrollTop: $("#cards").offset().top
    });

  }

 $(document).ready(function () {
    $("#btn_in_progress").click(function () {
      $("#cards").load("/progress");
      high_light_tab("btn_in_progress");
      scroll_to_cards();

    });

    $("#btn_created_by_me").click(function () {
      $("#cards").load("/created");
      high_light_tab("btn_created_by_me");
      scroll_to_cards();
    });

    $("#btn_shared_with_me").click(function () {
      $("#cards").load("/shared");
      high_light_tab("btn_shared_with_me");
      scroll_to_cards();


    });

    $("#btn_archived").click(function () {
      $("#cards").load("/archived");
      high_light_tab("btn_archived");
      scroll_to_cards();

    });

    $("#btn_new_task").click(function () {
      show_new_task();
    //   $("#preview").load("/newtask");

    });

    $("#my_teams").click(function () {
      $("#cards").load("/teams");
      high_light_tab("");

    });


    $("#about").click(function () {
        $("#cards").load("/about");
        high_light_tab("");
  
      });

      $("#setting").click(function () {
        $("#cards").load("/setting");
        high_light_tab("");
  
      });
  });



window.onload = function () {
    var divtoload = $('#divtoload').text();
    var alertmsg = $('#alertmsg').text();
   
    if (divtoload == "loadteams") {
        $("#cards").load("/teams");

    }
    
    else if (divtoload == "loadcreatedtasks") {
        $("#cards").load("/created");
        high_light_tab("btn_created_by_me");

    }

    else if (divtoload == "shared") {
        $("#cards").load("/shared");
        high_light_tab("btn_shared_with_me");

    }
    
    else {
        $("#cards").load("/progress");
        high_light_tab("btn_in_progress");
    }
    if (alertmsg != ""){
        alert(alertmsg);
    }
    
    // show current date in published date
    document.getElementById("datepublish").valueAsDate = new Date();
   
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
;

/* show and hide div for new task  */
function show_new_task() {

    var dev_block = document.getElementById("preview");
    dev_block.style.display = "block";



   
};


function hide_new_task() {

    document.getElementById("datepublish").valueAsDate = new Date();
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


function fill_published_date(){
    // var field = document.getElementById('datepublish');
    // var date = new Date();
    
    // // Set the date
    // field.value = date.getFullYear().toString() + '-' + (date.getMonth() + 1).toString().padStart(2, 0) + 
    //     '-' + date.getDate().toString().padStart(2, 0);

    //     alert(field.value);

    // set input date valur to today date
   
}
