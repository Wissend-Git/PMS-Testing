$(document).ready(function() {
	$('#otp_form p#error_otp').css('display', 'none');
});

var session_otp_pass = session_otp_collect;

$('#otp_form .otp_form_close').on('click', function(){
    window.location.href = '/logout';
});

$("#otp_form button[type='submit']").on("click", function(event){
	let page_otp = $('#otp_form input[name="otp_getter"]').val()
	if (page_otp.length == 6){
		if (isNaN(page_otp) == false){
		    if(page_otp.toString() == session_otp_pass.toString()){
		    	$('#otp_form p#error_otp').css('display', 'none');
		    }else{
		    	$('#otp_form p#error_otp').css('display', 'block');
		    	$('#otp_form p#error_otp').text('Please enter the valid OTP')
		    	event.preventDefault();
		    }
		}else{
			$('#otp_form p#error_otp').css('display', 'block');
			$('#otp_form p#error_otp').text('Please enter OTP numbers only')
			event.preventDefault();
		}
	}else{
		$('#otp_form p#error_otp').css('display', 'block');
		if (page_otp.length > 6){
			$('#otp_form p#error_otp').text('Please enter only 6-digits')
		}else if(page_otp.length < 6){
			$('#otp_form p#error_otp').text('6-digits OTP number is must')
		}
		event.preventDefault();
	}
});

// function otp_container(){
//     var otp_form_dict = {}
//     let recover_wiss_id = $("input[name='recover_wiss_id']").val();
//     if(recover_wiss_id.trim() != ""){
//         let code_otp = (Math.round((Math.random()*(999999-100000)+100000), 0))
//         otp_form_dict['recover_wiss_id'] = recover_wiss_id
//         otp_form_dict['recover_wiss_otp'] = code_otp
//         $("input[name='generated_otp']").val(code_otp)
//         // event.preventDefault();
//     }
//     $.ajax({url: '/confirm_otp', type: 'POST', data: otp_form_dict, success: function(response){}, error: function(response){}});
// };