var data_storage = JSON.parse(my_storage);
var acknow_level = JSON.parse(acknow_state);

$(document).ready(function($){
    
    document.onkeydown = function(e){
        if(e.keyCode == 27){
            $("#acknowModel").fadeOut(1000);
            window.location.href = '/team_lead';
        }
    }

    $('#addon_creation').css('display','block');
    $('button.process_tab_link').css({'color':'#fff','background-color': '#00b1b3', 'font-size': '14px', 'font-weight': '600'})
});


/* ################################################################ Tab Movement ################################################################ */
// function moveReport(evt, tabname){
//     var iter, tabcontent, tablinks;
//     if(tabname == 'addon_process'){
//         $('#addon_creation').css('display','block');
//         $('#shift_assign_tab').css('display','none');
//         $('#shift_show_tab').css('display','none');
//         $('#newuser_station_tab').css('display','none');
//         $('button.process_tab_link').css({'color':'#fff','background-color': '#00b1b3', 'font-size': '14px', 'font-weight': '600'})
//         $('button.shift_assign_tab_link').css({'color':'#000','background-color': 'transparent', 'font-size': '13px', 'font-weight': '600'})
//         $('button.shift_show_tab_link').css({'color':'#000','background-color': 'transparent', 'font-size': '13px', 'font-weight': '600'})
//         $('button.newuser_tab_link').css({'color':'#000','background-color': 'transparent', 'font-size': '13px', 'font-weight': '600'})
//     }else if(tabname == 'addon_shift_assign'){
//         $('#addon_creation').css('display','none');
//         $('#shift_assign_tab').css('display','block');
//         $('#shift_show_tab').css('display','none');
//         $('#newuser_station_tab').css('display','none');
//         $('button.process_tab_link').css({'color':'#000','background-color': 'transparent', 'font-size': '13px', 'font-weight': '600'})
//         $('button.shift_assign_tab_link').css({'color':'#fff','background-color': '#00b1b3', 'font-size': '14px', 'font-weight': '600'})
//         $('button.shift_show_tab_link').css({'color':'#000','background-color': 'transparent', 'font-size': '13px', 'font-weight': '600'})
//         $('button.newuser_tab_link').css({'color':'#000','background-color': 'transparent', 'font-size': '13px', 'font-weight': '600'})
//     }else if(tabname == 'addon_shift_show'){
//         $('#addon_creation').css('display','none');
//         $('#shift_assign_tab').css('display','none');
//         $('#shift_show_tab').css('display','block');
//         $('#newuser_station_tab').css('display','none');
//         $('button.process_tab_link').css({'color':'#000','background-color': 'transparent', 'font-size': '13px', 'font-weight': '600'})
//         $('button.shift_assign_tab_link').css({'color':'#000','background-color': 'transparent', 'font-size': '13px', 'font-weight': '600'})
//         $('button.shift_show_tab_link').css({'color':'#fff','background-color': '#00b1b3', 'font-size': '14px', 'font-weight': '600'})
//         $('button.newuser_tab_link').css({'color':'#000','background-color': 'transparent', 'font-size': '13px', 'font-weight': '600'})
//     }else if(tabname == 'addon_newuser'){
//         $('#addon_creation').css('display','none');
//         $('#shift_assign_tab').css('display','none');
//         $('#shift_show_tab').css('display','none');
//         $('#newuser_station_tab').css('display','block');
//         $('button.process_tab_link').css({'color':'#000','background-color': 'transparent', 'font-size': '13px', 'font-weight': '600'})
//         $('button.shift_assign_tab_link').css({'color':'#000','background-color': 'transparent', 'font-size': '13px', 'font-weight': '600'})
//         $('button.shift_show_tab_link').css({'color':'#000','background-color': 'transparent', 'font-size': '13px', 'font-weight': '600'})
//         $('button.newuser_tab_link').css({'color':'#fff','background-color': '#00b1b3', 'font-size': '14px', 'font-weight': '600'})
//     }
// }
/* ################################################################ Tab Movement ################################################################ */

window.onclick = function(event){
    if (event.target == document.getElementById("acknowModel")){
        $('#acknowModel').attr("style","display: none");
        window.location.href = '/team_lead';
    }
}

$('#acknowModel .close').on('click', function(){
    $('#acknowModel').attr("style","display: none");
    window.location.href = '/team_lead';
})