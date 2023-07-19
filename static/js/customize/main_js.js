$(document).ready(function() {

    // date picker
    $('.input-daterange').datepicker({
        format: 'dd-mm-yyyy',
        autoclose: true
    });

    //today date
    var today_date = new Date();
    var month_names = ["Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sep", "Oct", "Nov", "Dec"];
    var week_days = {'0':'Sunday', '1':'Monday', '2':'Tuesday', '3':'Wednesday', '4':'Thursday', '5':'Friday', '6':'Saturday'};
    var month = month_names[today_date.getMonth()];
    var day = today_date.getDate();
    var week = today_date.getDay();
    var date_format = week_days[week]+", "+(day<10 ? '0':'')+day+' '+(month<10 ? '0':'')+month+' '+today_date.getFullYear();
    $("#today_date").text(date_format);

    document.onkeydown = function(e){
        if(e.keyCode == 27){
            $("#popup_image").fadeOut(1000);
        }
        if(e.keyCode == 37){
            plusSlides(37)
        }
        if(e.keyCode == 39){
            plusSlides(39)
        }
    }

    if(data_storage['template_image_path']['Open Images'].length != 0){
        $("#popup_image").css('display','block');
        $('#event_blog').css('display','none');
    }else{
        $("#popup_image").css('display','none');
        $('#event_blog').css('display','block');
    }

    if(data_storage['emp_type'] == 'PU'){
        $('#project_filter #select_report_type').css('margin','0px 10px 0px 35px');
        $('#project_filter #select_report_type li').css('margin','3px 10px');
    }else{
        $('#project_filter #select_report_type').css('margin','0px 15px 0px 25px');
        $('#project_filter #select_report_type li').css('margin','3px 6px');
    }

    remove_duplicates_select("#user_selected #myFilter option");
    remove_duplicates_select("#kra_dropdown #myFilter1 option");
    remove_duplicates_select("#log_dropdown #log_user_filter select[name='log_user_selected'] option");

    // check project select after page loaded
    let project_selected_report = $('#project_selected_report select').val();
    if (project_selected_report == ""){
        $('#process_selected_report').css('display', 'none');
        $('#check_team_user').css('display', 'none');
        $('#user_selected').css('display', 'none');
    }else{
        $('#process_selected_report').css('display', 'block');
        $('#process_selected_report option').css('display', 'none');
        $('#process_selected_report option[value^="'+project_selected_report+'_"], #process_selected_report option[value="All"]').css('display', 'block');
        $('#process_selected_report option[value^="'+project_selected_report+'_Quality Check"]').css('display', 'none');
        $('#check_team_user').css('display', 'block');
        if (project_selected_report != "All"){
            $('#user_selected select option').each(function(){
                let option_val = $(this).val();
                if (option_val.includes(project_selected_report+'_') == true || option_val == "All" || option_val == ""){
                    $(this).css('display', 'block');
                }else{
                    $(this).css('display', 'none');
                }
            });
        }else{
            $('#user_selected select option').css("display",'block');
        }
    }
    
    // check project select user after page loaded
    let project_selected_user = $('#project_selected_user select').val();
    if (project_selected_user != ""){
        $('#process_selected_user').css('display', 'block');
        $('#process_selected_user option').css('display', 'none');
        $('#process_selected_user option[value^="'+project_selected_user+'_"]').css('display', 'block');
    }else{
        $('#process_selected_user').css('display', 'none');
    }

    // check user select after page loaded
    let check_user_status = $("#check_user").is(":checked");
    if (check_user_status == true){
        $('#user_selected').css('display', 'block');
        $('#user_selected option[value=""]').prop('checked', true);
    }else{
        $('#check_user').prop('checked', false);
        $('#user_selected').css('display', 'none');
    }

    //checking year, month, week, day are checked or unchecked after page loaded
    let select_year = $('#summary_form #check_year').is(":checked");
    let select_month = $('#summary_form #check_month').is(":checked");
    let select_week = $('#summary_form #check_week').is(":checked");
    let select_day = $('#summary_form #check_day').is(":checked");
    if(select_year == false && select_month == false && select_week == false && select_day == false){
        $('#summary_form #check_month').prop('checked', true);
    }

    let log_user_data = $("#project_selected_log #log_project").val();
    if (log_user_data == ""){
        $("#log_user_filter").css("display","none");
    }

    let kra_input_status = $("#kra_input").is(":checked");
    if (kra_input_status == true){
        $("#kra_report").prop('checked', false);
        if(['ADMIN','TA','TBH','TBHR'].includes(data_storage['emp_type'])){
            $("#kra_dropdown #kra_month_range").css("display","block");
            $('select[name="kra_user_selected"] option[value="All"]').css("display","none");
        }else{
            $("#kra_dropdown #kra_month_range").css("display","none");
            $('select[name="kra_user_selected"] option[value="All"]').css("display","block");
        }
    }

    let kra_report_status = $("#kra_report").is(":checked");
    if (kra_report_status == true){
        $("#kra_input").prop('checked', false);
        $("#kra_dropdown #kra_month_range").css("display","block");
    }

    let header_height = $('#tool_header .header_block').height();
    $("#data_table thead tr th").css("top",header_height);

    sort_select_option("#log_dropdown #log_project",3);
    sort_select_option("#project_filter #production_project",2);
    sort_select_option("#project_filter #production_process",2);
    sort_select_option("#project_filter #productivity_project",3);
    sort_select_option("#project_filter #productivity_process",3);
    
    $("#production_date").datepicker('setDate', new Date());
    $("#quality_date").datepicker('setDate', new Date());

    if(data_storage['report_type'] == 'Quality Assurance'){
        $('.report_content #user_report').css('display','none');
        $('.report_content #file_report').css('display','block');
    }else{
        $('.report_content #user_report').css('display','block');
        $('.report_content #file_report').css('display','none');
    }

    
});

var data_storage = JSON.parse(my_storage);

// ######################### modified images ########################################
$('.event_close').on('click', function(){$('#event_blog').fadeOut(1000);});
$('#popup_image .close').on('click', function(){$('#popup_image').fadeOut(1000);});

$('#event_blog a.event_visible').on('click', function(){
    $('#event_blog').fadeOut(1000);
    $("#popup_image").fadeIn(1000);
});

var slideIndex = 1;
showSlides(slideIndex);

function plusSlides(n){
    if(n == 37){
        n = -1;
    }else if(n == 39){
        n = 1;
    }
    showSlides(slideIndex += n);
}

function showSlides(n){
    var i;
    var slides = document.getElementsByClassName("mySlides");
    if (n > slides.length){slideIndex = 1}
    if (n < 1){slideIndex = slides.length}
    for (i = 0; i < slides.length; i++) {
      slides[i].style.display = "none";
    }
    if(slides.length != 0){
        slides[slideIndex-1].style.display = "block";
    }
}
// ######################### modified images ########################################

//left menu box full page height
$( window ).resize(function(){
    let window_height = $(window).height();
    let header_height = $('#tool_header .header_block').height();
    $('body').css('height', (window_height));
    $(".body_bckgrnd").css({'padding-top':header_height}) ;
    let right_body = $(".body_bckgrnd").height();
    if (right_body < window_height){
        $(".body_bckgrnd").css({'height':window_height}) ;
        // $(".body_bckgrnd").css({'height':'auto'}) ;
    }
});
$(window).trigger('resize');

// $(".body_bckgrnd").resize(function(){
//     let window_height = $(window).height();
//     let header_height = $('#tool_header .header_block').height();
//     // $('body').css('height', (window_height));
//     $(".body_bckgrnd").css({'padding-top':header_height,'height':window_height}) ;
//     // $(".body_bckgrnd").css({'height':window_height}) ;
// });
// $(".body_bckgrnd").trigger('resize');


//left menu click color change
$('#project_filter .card a').on('click', function(){
    let a_tag = $(this).text();
    if (a_tag.includes("Profile")){
        if (data_storage['employee_designation'] in ['Data Analyst','Senior Data Analyst']){
            window.location.href = '/employee_page';
        }else{
            window.location.href = '/team_lead';
        }
    }
    if (a_tag.includes("Production")){
        window.location.href = '/production';
    }
    if (a_tag.includes("Add-On")){
        window.location.href = '/addon';
    }
    if (a_tag.includes("Gallery")){
        window.location.href = '/gallery';
    }
    if (a_tag.includes("Leave")){
        window.location.href = '/leave_request';
    }
    if(a_tag.includes("Employees Entry")){
        window.location.href = '/emp_entry';
    }
    $('#project_filter .card').each(function(){
        let card_class = $(this).attr('class');
        let str_class = card_class.toString();
        if(str_class.includes("menu_active") == true ){
            $(this).removeClass('menu_active');
            $(this).css('background-color','#00abad');
        }
    });
    $(this).parent().parent('.card').addClass("menu_active");
});

// #######################################################################################################################
$('.report_card a').on('click', function(){
    let a_tag = $(this).text();
    $('.report_card').each(function(){
        let card_class = $(this).attr('class');
        let str_class = card_class.toString();
        if(str_class.includes("menu_active") == true ){
            $(this).removeClass('menu_active');
            $(this).css('background-color','#00abad');
        }
    });
    $(this).parent().parent('.card').addClass("menu_active");
});
// #######################################################################################################################

// after project selected
$('#project_selected_report select').on('change', function(){
    $('#project_error_text').text('');
    let project_selected_report = $('#project_selected_report select').val();
    if (project_selected_report != "All"){
        $('#process_selected_report').css('display', 'block');
        $('#process_selected_report option').css('display', 'none');
        $('#process_selected_report option[value^="'+project_selected_report+'_"], #process_selected_report option[value="All"], #process_selected_report option[value=""]').css('display', 'block');
        $('#process_selected_report option[value^="'+project_selected_report+'_Quality Check"]').css('display', 'none');
        $('#check_team_user').css('display', 'block');
        $('#user_selected select option').each(function(){
            let option_val = $(this).val();
            if (option_val.includes(project_selected_report+'_') == true || option_val == "All"){
                $(this).css('display', 'block');
            }else{
                $(this).css('display', 'none');
            }
        });
    }else if (project_selected_report == "All"){

        $('#process_selected_report').css('display', 'block');
        $('#process_selected_report option').css('display', 'none');
        $('#process_selected_report option[value="All"], #process_selected_report option[value=""]').css('display', 'block');
        $('#check_team_user').css('display', 'block');
        $('#user_selected select option').css('display','block');
        remove_duplicates_select("#user_selected #myFilter option");
    }
});

// after project user selected
$('#project_selected_user select').on('change', function(){
    $('#project_error_text_user').text('');
    let project_selected_user = $('#project_selected_user select').val();
    if (project_selected_user != ""){
        $('#process_selected_user').css('display', 'block');
        $('#process_selected_user option').css('display', 'none');
        $('#process_selected_user option[value^="'+project_selected_user+'_"]').css('display', 'block');
    }
});


// after project user selected
$('#project_selected_log select').on('change', function(){
    $('#project_error_text_user').text('');
    let project_selected = $(this).val();
    if (project_selected != ""){
        $('#log_user_filter').css('display', 'block');
        if (project_selected == "All"){
            $('#log_user_filter option').css('display', 'block');
        }else{
            $('#log_user_filter option').css('display', 'none');
            $('#log_user_filter option[value="All"], #log_user_filter option[value^="'+project_selected+'_"]').css('display', 'block');
        }
    }else{
        $('#log_user_filter').css('display', 'none');
    }
    remove_duplicates_select("#log_dropdown #log_user_filter select[name='log_user_selected'] option")
});


// after user selected
$("#check_user").on('click', function(){
    let check_user_status = $("#check_user").is(':checked');
    if (check_user_status == true){
        $('#user_selected').css('display', 'block');
    }else{
        $('#user_selected select option[value=""]').prop('selected', true);
        $('#user_selected').css('display', 'none');
    }
});

// clear error text after process, user selected
$("#process_selected_report select, #user_selected select").on('change', function(){
    $('#project_error_text').text('');
});

$("#user_selected select").on('change', function(){
    $('#project_error_text').text('');
});

//after year clicked
$('#summary_form #check_year').on('click', function(){
    let select_year = $('#summary_form #check_year').is(":checked");
    if (select_year == true){
        $('#summary_form #check_month').prop('checked', false);
        $('#summary_form #check_week').prop('checked', false);
        $('#summary_form #check_day').prop('checked', false);
        $('#date_error_text').css('display','none');
    }
});

//after month clicked
$('#summary_form #check_month').on('click', function(){
    let select_month = $('#summary_form #check_month').is(":checked");
    if (select_month == true){
        $('#summary_form #check_year').prop('checked', false);
        $('#summary_form #check_week').prop('checked', false);
        $('#summary_form #check_day').prop('checked', false);
        $('#date_error_text').css('display','none');
    }
});

//after week clicked
$('#summary_form #check_week').on('click', function(){
    let select_week = $('#summary_form #check_week').is(":checked");
    if (select_week == true){
        $('#summary_form #check_year').prop('checked', false);
        $('#summary_form #check_month').prop('checked', false);
        $('#summary_form #check_day').prop('checked', false);
        $('#date_error_text').css('display','none');
    }
});

//after day clicked
$('#summary_form #check_day').on('click', function(){
    let select_day = $('#summary_form #check_day').is(":checked");
    if (select_day == true){
        $('#summary_form #check_year').prop('checked', false);
        $('#summary_form #check_week').prop('checked', false);
        $('#summary_form #check_month').prop('checked', false);
        $('#date_error_text').css('display','none');
    }
});

// Quality Controls ///////////////////////////////////////////////////////////
//after productivity clicked
$('#project_filter #select_report_type #productivity_report').on('click', function(){
    let productivity_report = $('#project_filter #select_report_type #productivity_report').is(":checked");
    if (productivity_report == true){
        $('#project_filter #select_report_type #team_quality').prop('checked', false);
        $('#project_filter #select_report_type #user_quality').prop('checked', false);
        $('#project_filter #select_report_type #assure_quality').prop('checked', false);
        $('#date_error_text').css('display','none');
    }
});

//after team quality clicked
$('#project_filter #select_report_type #team_quality').on('click', function(){
    let team_quality = $('#project_filter #select_report_type #team_quality').is(":checked");
    if (team_quality == true){
        $('#project_filter #select_report_type #productivity_report').prop('checked', false);
        $('#project_filter #select_report_type #user_quality').prop('checked', false);
        $('#project_filter #select_report_type #assure_quality').prop('checked', false);
        $('#date_error_text').css('display','none');
    }
});

//after user quality clicked
$('#project_filter #select_report_type #user_quality').on('click', function(){
    let user_quality = $('#project_filter #select_report_type #user_quality').is(":checked");
    if (user_quality == true){
        $('#project_filter #select_report_type #productivity_report').prop('checked', false);
        $('#project_filter #select_report_type #team_quality').prop('checked', false);
        $('#project_filter #select_report_type #assure_quality').prop('checked', false);
        $('#date_error_text').css('display','none');
    }
});

//after quality assurance clicked
$('#project_filter #select_report_type #assure_quality').on('click', function(){
    let assure_quality = $('#project_filter #select_report_type #assure_quality').is(":checked");
    if (assure_quality == true){
        $('#project_filter #select_report_type #productivity_report').prop('checked', false);
        $('#project_filter #select_report_type #team_quality').prop('checked', false);
        $('#project_filter #select_report_type #user_quality').prop('checked', false);
        $('#date_error_text').css('display','none');
    }
});
// Quality Controls ///////////////////////////////////////////////////////////


//left menu report user submit check
$('#project_submit_user').on('click', function(event){
    let project_selected = $('#project_selected_user select').val();
    if (project_selected != ""){
        let process_selected = $('#process_selected_user select').val();
        if (process_selected == ""){
            $('#project_error_text_user').text('Please select the process');
            event.preventDefault();
        }else{
            let process_list = Object.keys(data_storage['employee_projects'][project_selected]['process'])
            let process_selected_list = process_selected.split("_")
            let process_selected_data = process_selected_list[process_selected_list.length - 1]
            if (process_list.includes(process_selected_data) == false) {
                $('#project_error_text_user').text('Please select the correct process');
                event.preventDefault();
            }
        }
    }else{
        $('#project_error_text_user').text('Please select the process');
        event.preventDefault();
    }
});

// quality Controls
//left menu report submit check
$('#project_submit').on('click', function(event){
    let productivity_selected = $('#project_filter #select_report_type #productivity_report').is(':checked')
    let teamq_selected = $('#project_filter #select_report_type #team_quality').is(':checked')
    let userq_selected = $('#project_filter #select_report_type #user_quality').is(':checked')
    let assureq_selected = $('#project_filter #select_report_type #assure_quality').is(':checked')
    if(productivity_selected == false && teamq_selected == false && userq_selected == false && assureq_selected == false){
        $('#project_error_text').text("Please select the report type");
        event.preventDefault(); 
    }else{
        let project_selected = $('#project_selected_report select').val();
        if (project_selected != ""){
            let process_selected = $('#process_selected_report select').val();
            if (process_selected == ""){
                $('#project_error_text').text('Please select the process');
                event.preventDefault();
            }else{
                let check_user_status = $("#check_user").is(':checked');
                if (check_user_status == true){
                    let user_selected = $("#user_selected select").val();
                    if (user_selected == "" || user_selected.length == 0){
                        $('#project_error_text').text("Please select the user");
                        event.preventDefault();
                    }
                }
            }
        }else{
            $('#project_error_text').text('Please select the project');
            event.preventDefault();
        }
    }

});
// quality Controls

//left menu report reset button
$('#reset_submit').on('click', function(){
    $('#project_selected_report select').val("");
    $('#process_selected_report select').val("");
    $('#user_selected').css('display', 'none');
    $('#selected_year select').val("");
    $('#selected_month select').val("");
    $('#check_month').prop("checked", true);
    $("#from_date").datepicker('setDate', null);
    $("#to_date").datepicker('setDate', null);
});

//reset from and to date when year is selected
$('#selected_year').on('change', function(){
    let selected_year = $(this).find(":selected").text();
    if ($("#from_date").val() != ""){
        $("#from_date").datepicker('setDate', null);
        $("#to_date").datepicker('setDate', null);
    }
    $('#selected_year select option[value="'+selected_year+'"]').prop('selected', 'true');
});

//reset from and to date when month is selected
$('#selected_month').on('change', function(){
    let selected_month = $(this).find(":selected").text();
    if ($("#from_date").val() != ""){
        $("#from_date").datepicker('setDate', null);
        $("#to_date").datepicker('setDate', null);
    }
    $('#selected_month select option[value="'+selected_month+'"]').prop('selected', 'true');
});

//reset year and month when from date is selected
$('#from_date').on('change',function(){
    $('#selected_year select option[value=""]').prop('selected', 'true');
    $('#selected_month select option[value=""]').prop('selected', 'true');
});


//change password
$(".change_pswd #create_password").on('change', function(event){
    let new_pswd = $(this).val().trim();
    if (new_pswd == ""){
        $('.change_pswd .error_text').text("Don't leave Password empty");
        event.preventDefault();
    }else{
        if (new_pswd.length < 10){
            $('.change_pswd .error_text').text("Your Password should have more than 10 characters");
            event.preventDefault();
        }else{
            let new_pswd = $(this).val().trim();
            let i = 0;
            let upper_count = 0;
            let lower_count = 0;
            let spl_char_count = 0;
            for(i=0;i<new_pswd.length;i++){
                let char_data = new_pswd[i];
                let check_type = check_alpha(char_data);
                if (char_data == char_data.toUpperCase() && check_type == true){
                    upper_count++;
                }
                if (char_data == char_data.toLowerCase() && check_type == true){
                    lower_count++;
                }
                let spl_char = ['$','#','@','!','%','^','&','*','(',')'];
                if (spl_char.includes(char_data)){
                    spl_char_count++;
                }
            }
            if (upper_count == 0 || lower_count == 0 || spl_char_count == 0){
                if (upper_count == 0){
                    $('.change_pswd .error_text').text("Your Password should have atleast one Uppercase letter");
                }else if (lower_count == 0){
                    $('.change_pswd .error_text').text("Your Password should have atleast one Lowercase letter");
                }else if (spl_char_count == 0){
                    $('.change_pswd .error_text').text("Your Password should have atleast one Special character");
                }
            }else{
                $('.change_pswd .error_text').text("");
            }
        }
    }
});

//change password
$(".change_pswd button").on('click', function(event){
    let new_pswd = $(".change_pswd #create_password").val().trim();
    let confirm_pswd = $(".change_pswd #confirm_password").val().trim();
    if (new_pswd == "" || confirm_pswd == ""){
        $('.change_pswd .error_text').text("Don't leave Password empty")
        event.preventDefault();
    }else{
        if (new_pswd.length < 10 || confirm_pswd.length < 10){
            $('.change_pswd .error_text').text("Your Password should have more than 10 characters");
            event.preventDefault();
        }else{
            let i = 0;
            let upper_count = 0;
            let lower_count = 0;
            let spl_char_count = 0;
            let int_count = 0;
            for(i=0;i<new_pswd.length;i++){
                let char_data = new_pswd[i];
                let spl_char = ['$','#','@','!','%','^','&','*','(',')'];
                if (char_data == char_data.toUpperCase() && isNaN(char_data) == true && spl_char.includes(char_data) == false){
                    upper_count++;
                }
                if (char_data == char_data.toLowerCase() && isNaN(char_data) == true && spl_char.includes(char_data) == false){
                    lower_count++;
                }
                if (spl_char.includes(char_data)){
                    spl_char_count++;
                }
                if (isNaN(char_data) == false && spl_char.includes(char_data) == false){
                    int_count++;
                }
            }
            if (upper_count == 0 || lower_count == 0 || spl_char_count == 0 || int_count == 0){
                if (upper_count == 0){
                    $('.change_pswd .error_text').text("Your new Password should have atleast one Uppercase letter");
                }else if (lower_count == 0){
                    $('.change_pswd .error_text').text("Your new Password should have atleast one Lowercase letter");
                }else if (spl_char_count == 0){
                    $('.change_pswd .error_text').text("Your new Password should have atleast one Special character");
                }else{
                    $('.change_pswd .error_text').text("Your new Password should have atleast one Numeric Number");
                }
                event.preventDefault();
            }else{
                if (new_pswd != confirm_pswd){
                    $('.change_pswd .error_text').text("Password not matched. Please type correct password");
                    event.preventDefault();
                }else{
                    $('.change_pswd .error_text').text("");
                }
            }
        }
    }
});

$("#kra_submit").on('click', function(event){
    $("#kra_error_text_user").text("");
    let kra_status = $("#kra_input").is(":checked");
    let report_status = $("#kra_report").is(":checked");
    let select_val = $("#kra_dropdown select").val();
    if (select_val == ""){
        $("#kra_error_text_user").text("Please select the user");
        event.preventDefault();
    }else if(select_val == "All" && kra_status == true) {
        $("#kra_error_text_user").text("select any one employee");
        event.preventDefault();
    }else if (kra_status == false && report_status == false){
        $("#kra_error_text_user").text("select type input or report");
        event.preventDefault();
    }
    if(['ADMIN','TA','TBH','TBHR'].includes(data_storage['emp_type'])){
        if(kra_status == true && report_status == false){
            if($('#kra_month_range select[name="kra_year_selected"]').val() == ''){
                $("#kra_error_text_user").text("select the input year");
                event.preventDefault();
            } 
        }
    }
    if (report_status == true){
        $('#kra_dropdown #kra_month_range select[name="kra_year_selected"]').val();
    }
});

$("#check_kra_type input").on('click', function(){
    let kra_id = $(this).attr("id");
    if (kra_id == "kra_input"){
        var kra_next_id = "#kra_report";
    }else{
        var kra_next_id = "#kra_input";
    }
    let kra_status = $(this).is(":checked");
    if (kra_status == true){
        $(kra_next_id).prop('checked', false);
    }else{
        $(kra_next_id).prop('checked', true);
    }
    if(kra_id == "kra_report" && kra_status == true){
        $("#kra_dropdown #kra_month_range").css("display","block");
        $('select[name="kra_user_selected"] option[value="All"]').css("display","block");
        $('#kra_month_range #kra_selected_year select option[value="All"], #kra_month_range #kra_selected_month select option[value="All"]').css('display', 'block');
    }else if(kra_id == "kra_input" && kra_status == true && ['ADMIN','TA','TBH','TBHR'].includes(data_storage['emp_type'])){
        $("#kra_dropdown #kra_month_range").css("display","block");
        $('select[name="kra_user_selected"] option[value="All"]').css("display","none");
        $('#kra_month_range #kra_selected_year select option[value="All"], #kra_month_range #kra_selected_month select option[value="All"]').css('display', 'none');
        $('#kra_dropdown #kra_month_range select[name="kra_year_selected"] option, #kra_dropdown #kra_month_range select[name="kra_month_selected"] option').each(function(){
            if (this.value.length == 0){
                $(this).prop("selected",true);
            }else{
                $(this).prop("selected",false);
            }
        });
    }else{
        $("#kra_dropdown #kra_month_range").css("display","none");
        $('select[name="kra_user_selected"] option[value="All"]').css("display","none");
        $('#kra_dropdown #kra_month_range select[name="kra_year_selected"] option, #kra_dropdown #kra_month_range select[name="kra_month_selected"] option').each(function(){
            if (this.value.length == 0){
                $(this).prop("selected",true);
            }else{
                $(this).prop("selected",false);
            }
        });
    }
});

function remove_duplicates_select(css_selector){
    let data_list = [];
    $(css_selector).each(function(){
        if (css_selector.includes("user_selected")){
            let user_id_val = $(this).attr("value");
            let user_id_val_split = user_id_val.split("_");
            var user_id = user_id_val_split[user_id_val_split.length-1];
        }else{
            var user_id = $(this).attr("value");
        }
        if (data_list.includes(user_id) == false){
            data_list.push(user_id);
        }else{
            $(this).css('display','none');
            // $(this).remove();
        }
    });
    sort_select_option(css_selector, 3);
}

function sort_select_option(css_selector, start_index){
    let css_selector_list = css_selector.split(" option");
    let css_selector_name = css_selector_list[0];
    $(css_selector_name).append($(css_selector_name+" option:nth-child(1n+"+start_index+")").remove().sort(function(a, b) { 
        var at = $(a).text(), 
            bt = $(b).text();
        if (isNaN(at) == false && isNaN(bt) == false){
            at = parseInt(at);
            bt = parseInt(bt);
        }
        return (at > bt) ? 1 : ((at < bt) ? -1 : 0); 
    }));
}

$("#log_submit, #log_summary").on("click", function(event){
    let log_project = $("#project_selected_log select").val();
    if (log_project == ""){
        $("#log_error_text").text("Select the project");
        event.preventDefault();
    }else{
        let log_user = $("#log_user_filter select").val();
        if (log_user == ""){
            $("#log_error_text").text("Select the user");
            event.preventDefault();
        }
    }
});


$("#attd_submit").on('click', function(e){
    $("#attd_error_text").text("");
    if(['ADMIN','TA','TBH','TBHR'].includes(data_storage['emp_type'])){
        if ($("#attd_from_date").val() == "" && $("#attd_to_date").val() == ""){
        $("#attd_error_text").text("Select the date");
        e.preventDefault();
        }
    }
});
