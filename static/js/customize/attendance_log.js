$(document).ready(function($){
    let logon_status = $("#log_on_block span").text();
    if (logon_status == "Yet to submit"){
        $("#log_off_block").css("display", "none");
    }else{
        $("#log_on_block button").prop('disabled',true);
        $("#log_on_block button").css({"background-color":"#cdcccc", "border":"1px solid #cdcccc"});
        $("#log_on_block span").css("color", "#087f32");
    }

    let logoff_status = $("#log_off_block").attr('data-attribute');
    if(logoff_status == 'Success'){
        $("#log_on_block button").prop('disabled',true);
        $("#log_off_block button").prop('disabled',true);
        $("#log_off_block button").css({"background-color":"#cdcccc", "border":"1px solid #cdcccc"});
        $(".attendance_block #log_total_block p").css({"background-color":"#9fdf9f", "border":"2px solid #9fdf9f", "color":"#000", "box-shadow": "0 3px 10px -3px #292929"});
        $("#log_off_block span").css("color", "#087f32");
    }
});


$("#log_on_block button").confirm({
    title: 'Attendance!',
    content: 'Are you confirm to log on?',
    type: 'green',
    typeAnimated: true,
    buttons: {
        tryAgain: {
            text: 'Confirm',
            btnClass: 'btn-green',
            action: function(){
                $.ajax({
                    url: '/attd_mark',
                    type: 'POST',
                    data: JSON.stringify({"log_on": "Success","log_off":"Yet to submit"}),
                    contentType: 'application/json',
                    success: function(response) {
                        location.reload();
                    },
                    error: function(error) {
                        console.log("e",error);
                    }
                });
            }
        },
        close: function () {
        }
    }
});

$("#log_off_block button").confirm({
    title: 'Submit Alert!',
    content: 'Are you confirm to log off?',
    type: 'red',
    typeAnimated: true,
    buttons: {
        tryAgain: {
            text: 'Confirm',
            btnClass: 'btn-red',
            action: function(){
                $.ajax({
                    url: '/attd_mark',
                    type: 'POST',
                    data: JSON.stringify({"log_on": "Submitted","log_off":"Submitted"}),
                    contentType: 'application/json',
                    success: function(response) {
                        location.reload();
                    },
                    error: function(error) {
                        console.log(error);
                    }
                });
            }
        },
        close: function () {
        }
    }
});

$('.entries_summary .attendance_notlogin').on('click', function(){
  $("#popup_notlogin_users").fadeIn(1000);
});

$('.entries_summary .attendance_logoff_times').on('click', function(){
  $("#popup_logout_users").fadeIn(1000);
});

$('#popup_notlogin_users .popup_entries_close').on('click', function(){
    $("#popup_notlogin_users").fadeOut(1000);
});

$('#popup_logout_users .popup_entries_close').on('click', function(){
    $("#popup_logout_users").fadeOut(1000);
});