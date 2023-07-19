$(document).ready(function() {

    // pre-loading screen if page time to load
    window.addEventListener('load', function () {
        $('body').addClass('loaded');
    });

    let window_height = $(window).height();
    let padding_height = (window_height/100)*25;
    $('.login_form').css("padding-top",padding_height);
    $('#error_wiss_id').css('display', 'none');
});

//login credentials check
$("#home_login button[type='submit']").on("click", function(event){
    let wiss_id = $("#home_login input[name='user_id']").val();
    let wiss_pswd = $("#home_login input[name='user_pswd']").val();
    if(wiss_id.trim() != "" && wiss_pswd.trim() != ""){
        if(wiss_id.trim().toLowerCase() === wiss_id){
            $("#error_text").text("Please enter propper User ID");
            event.preventDefault();
        }else{
            $("#error_text").text("");
            window.location.href = "/master";
        }
    }else{
        $("#error_text").text("Please enter both fields");
        event.preventDefault();
    }
});

$( window ).resize(function(){
    let window_height = $(window).height();
    let header_height = $('#tool_header .header_block').height();
    $('#change_pswd_content').css('height', (window_height-1)-header_height);
});
$(window).trigger('resize');

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

$('#home_login span.forgot_pwd').on('click', function(){
    $('#recovery_form').fadeIn(1000);
});

$('#recovery_form .recovery_form_close').on('click', function(){
    $('#recovery_form').fadeOut(1000);
});

$('#reset_pwd_form button[type=submit]').on('click', function(){
    let recover_wiss_id = $('#reset_pwd_form input[name="recover_wiss_id"]').val();
    let constrain_error = ''
    if(recover_wiss_id.length == 7){
        if(recover_wiss_id.toLowerCase() === recover_wiss_id){
            $('#error_wiss_id').css('display', 'block');
            $('#error_wiss_id').text("Enter Wissend ID in Propper Case..")
            event.preventDefault();
        }else{
            console.log(error_content_data)
            $('#error_wiss_id').css('display', 'none');
            // event.preventDefault();
        }
    }else{
        $('#error_wiss_id').css('display', 'block');
        $('#error_wiss_id').text("Not a Wissend ID")
        event.preventDefault();
    }
});

var check_icon = 0
function login_change_icon(){
    check_icon = check_icon+1
    if (check_icon % 2 == 0){
        $('#login_togglePassword').removeClass('fa-eye');
        $('#login_togglePassword').addClass('fa-eye-slash');
        $('#home_login input[name="user_pswd"]').attr('type', 'password');
    }else{
        $('#login_togglePassword').removeClass('fa-eye-slash');
        $('#login_togglePassword').addClass('fa-eye');
        $('#home_login input[name="user_pswd"]').attr('type', 'text');
    }
}
var create_icon = 0
function create_change_icon(){
    create_icon = create_icon+1
    if (create_icon % 2 == 0){
        $('#create_togglePassword').removeClass('fa-eye');
        $('#create_togglePassword').addClass('fa-eye-slash');
        $('.change_pswd input[name="new_password"]').attr('type', 'password');
    }else{
        $('#create_togglePassword').removeClass('fa-eye-slash');
        $('#create_togglePassword').addClass('fa-eye');
        $('.change_pswd input[name="new_password"]').attr('type', 'text');
    }
}
var confirm_icon = 0
function confirm_change_icon(){
    confirm_icon = confirm_icon+1
    if (confirm_icon % 2 == 0){
        $('#confirm_togglePassword').removeClass('fa-eye');
        $('#confirm_togglePassword').addClass('fa-eye-slash');
        $('.change_pswd input[name="confirm_new_password"]').attr('type', 'password');
    }else{
        $('#confirm_togglePassword').removeClass('fa-eye-slash');
        $('#confirm_togglePassword').addClass('fa-eye');
        $('.change_pswd input[name="confirm_new_password"]').attr('type', 'text');
    }
}
