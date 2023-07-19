$(document).ready(function(){

  $('.leave_application .for_leave_application').css('display', 'none')
  $('.leave_application .for_permission_application').css('display', 'none')
  $('.leave_application .for_od_application').css('display', 'none')
  $('.taking_and_balance_content').css('display', 'none')
  
  $('.availablities').css('display', 'none');
  $('#alert_modal').css('display','none');
  $('#approve_confirm').css('display', 'none');

  // defult - tab selection
  $('#leave_apply_tab').css('display','none');
  $('button.leave_status_tab_link').css({'color':'#fff','background-color': '#00b1b3', 'font-size': '14px', 'font-weight': '600'})

  // defult - table visibilty
  $('.leave_status_table').css('display', 'inline-flex');
  $('.permission_status_table').css('display', 'none');
  // defult - status color
  status_and_approval_color()
  PermissionTrack()
  LeaveBalanceAndSelection()
  // defult - status bar selection
  $('.status_bar_graph').css('display', 'none');

});

var today_date = new Date();
var month_names = ["Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sep", "Oct", "Nov", "Dec"];
var month = month_names[today_date.getMonth()];
var data_storage = JSON.parse(my_storage);
var leave_storage = JSON.parse(leave_data);

var applydays_for_date = 0
var final_applying_days = 0
var CurrentSelected_LeaveType = ''

$(".leave_block_segment").datepicker({"dateFormat" : "mm/dd/yyyy", 'autoclose': true});
$(".permission_block_segment").datepicker({"dateFormat" : "mm/dd/yyyy", 'autoclose': true});
$(".od_block_segment").datepicker({"dateFormat" : "mm/dd/yyyy", 'autoclose': true});

/* #################################### Alert Module */
$('.alert_modal_close').on('click', function(){
  $('#alert_modal').fadeOut(1000);
  cancel_execution()
  // window.location.href = '/leave_request';
});

/* #################################### Alert Module */
$('.approve_confirm_close').on('click', function(){
  $('#approve_confirm').fadeOut(1000);
});

/* ################################################################ Tab Movement ################################################################ */
function moveReport(evt, tabname){
    var iter, tabcontent, tablinks;
    if(tabname == 'leave_status_process'){
        $('#leave_status_tab').css('display','block');
        $('#leave_apply_tab').css('display','none');
        $('.taking_and_balance_content').css('display', 'none')
        $('button.leave_status_tab_link').css({'color':'#fff','background-color': '#00b1b3', 'font-size': '14px', 'font-weight': '600'})
        $('button.leave_apply_tab_link').css({'color':'#000','background-color': 'transparent', 'font-size': '13px', 'font-weight': '600'})
    }else if(tabname == 'leave_apply_process'){
        $('#leave_apply_tab').css('display','block');
        $('.taking_and_balance_content').css('display', 'flex')
        $('#leave_status_tab').css('display','none');
        $('button.leave_apply_tab_link').css({'color':'#fff','background-color': '#00b1b3', 'font-size': '14px', 'font-weight': '600'})
        $('button.leave_status_tab_link').css({'color':'#000','background-color': 'transparent', 'font-size': '13px', 'font-weight': '600'})
    }
}
/* ################################################################ Tab Movement ################################################################ */

function LeaveBalanceAndSelection(){
  let balance_storage = leave_storage[1]['Balance'];
  if(balance_storage['cl'] == '0.0'){$('.apply_for select[name="apply_type"] option[value="CL"]').hide();}
  if(balance_storage['sl'] == '0.0'){$('.apply_for select[name="apply_type"] option[value="SL"]').hide();}
  if(balance_storage['perm'] == '0.0'){$('.apply_for select[name="apply_type"] option[value="P"]').hide();}
  if(balance_storage['perm'] == '1.0' ){
    $('.perm_date_and_session select[name="perm_hours_type"] option[value="2hr"]').hide();
  }
}

function PermissionTrack(){
  let perm_taken = $('.taking_and_balance_content .balance_status li:nth-child(3) > span').text()
  if(perm_taken == '1.0'){
    $('.taking_and_balance_content .taking_status li:nth-child(3) > span.return_perm_bal').text("1.0")
  }else if(perm_taken == '2.0'){
    $('.taking_and_balance_content .taking_status li:nth-child(3) > span.return_perm_bal').text("0.0")
  }else{
    $('.taking_and_balance_content .taking_status li:nth-child(3) > span.return_perm_bal').text("0.0")
  }
}

/* ################################################################ Leave Application ################################################################ */
/* #################################### on change application type #################################### */
$('.leave_application .apply_for select').on('change', function(){
    let application_type = $(this).val();
    if(application_type == "CL" || application_type == "SL" || application_type == "SCL"){
      $('.leave_application .for_leave_application').css('display', 'block');
      $('.leave_application .for_permission_application').css('display', 'none')
      $('.leave_application .for_od_application').css('display', 'none')
      $('.availablities').css('display', 'block')
      $('.availablities .applying_days').css('display', 'inline-flex');
      $('.availablities .balance').css('display', 'none');
      $('.availablities .permission_hours').css('display', 'none');
    }else if(application_type == "P"){
      $('.leave_application .for_permission_application').css('display', 'block')
      $('.leave_application .for_leave_application').css('display', 'none')
      $('.leave_application .for_od_application').css('display', 'none')
      $('.availablities .permission_hours').css('display', 'inline-flex');
      $('.availablities .applying_days').css('display', 'none');
      $('.availablities .balance').css('display', 'none');
    }else if(application_type == "OD"){
      $('.leave_application .for_od_application').css('display', 'block')
      $('.leave_application .for_permission_application').css('display', 'none')
      $('.leave_application .for_leave_application').css('display', 'none')
      $('.availablities .permission_hours').css('display', 'none');
      $('.availablities .applying_days').css('display', 'none');
      $('.availablities .balance').css('display', 'none');
    }
    CurrentSelected_LeaveType = application_type
    DateAndSession_Clear()
    availablities_clear()
});

// #################################### inputs validation ####################################
function validate_input(){
    let check_list = 0
    let apply_type = ''
    let select_application_type = $('select[name="apply_type"]').val();
    if(select_application_type == ''){
      check_list = 1;
      apply_type = "Please select application type"
      return [check_list, apply_type];
    }else if(select_application_type == "SL" || select_application_type == "CL" || select_application_type == "SCL"){
      let from_date = $('.from_date_and_session #fromDate').val();
      let from_session = $('.from_date_and_session select[name="from_session_type"]').val();
      if (from_date.length == 0 || from_session.length == 0){
        check_list = 2;
        apply_type = "Please select the date & session"
        return [check_list, apply_type];
      }else{
        let to_date = $('.to_date_and_session #toDate').val();
        let to_session = $('.to_date_and_session select[name="to_session_type"]').val();
        if (to_date.length == 0 || to_session.length == 0){
          check_list = 3;
          apply_type = "Please select the date & session"
          return [check_list, apply_type];
        }else{
          let reson_check = $('.leave_reason textarea').val();
          if (reson_check.length == 0){
            check_list = 4;
            apply_type = "Please fill the reason is mandatory."
            return [check_list, apply_type];
          }
        }
      }
    }else if(select_application_type == "P"){
      let from_date = $('.for_permission_application #permDate').val();
      if (from_date.length == 0){
        check_list = 1;
        apply_type = "Please select the permission date as you need"
        return [check_list, apply_type];
      }else{
        let perm_hour_selection = $('.perm_date_and_session select[name="perm_hours_type"]').val();
        if (perm_hour_selection.length == 0){
            check_list = 2;
            apply_type = "Please pick your convenient hour."
            return [check_list, apply_type];
        }else{
          let reson_check = $('.leave_reason textarea').val();
          if (reson_check.length == 0){
            check_list = 5;
            apply_type = "Please fill the reason is mandatory."
            return [check_list, apply_type];
          }
        }
      }
    }else if(select_application_type == "OD"){
      let from_date = $('.for_od_application #odDate').val();
      if (from_date.length == 0){
        check_list = 1;
        apply_type = "Please select the OD date as you need"
        return [check_list, apply_type];
      }
    }
    return [check_list, apply_type]
};

function application_submit(event){
  let triger = validate_input()
  if(triger[0] != 0 && triger[1] != ''){
    $('#application_error_text').text(triger[1])
    event.preventDefault();
  }
}
/* ################################################################ Leave Application ################################################################ */

/* #################################### automate contents in page #################################### */
/* #################################### for days */
function ApplyingDaysForamtion(apply_enter_number){
  if($('.availablities .applying_days span').length == 0){
    if (apply_enter_number < 2){
      $('.availablities .applying_days').append('<span>'+apply_enter_number+' Day</span><input style="display: none;" name="num_of_days" id="num_of_days" type="text" value="'+apply_enter_number+'">')
    }else{
      $('.availablities .applying_days').append('<span>'+apply_enter_number+' Days</span><input style="display: none;" name="num_of_days" id="num_of_days" type="text" value="'+apply_enter_number+'">')
    }
  }else{
    $('.availablities .applying_days span').remove()
    $('.availablities .applying_days input').remove()
    if (apply_enter_number < 2){
      $('.availablities .applying_days').append('<span>'+apply_enter_number+' Day</span><input style="display: none;" name="num_of_days" id="num_of_days" type="text" value="'+apply_enter_number+'">')
    }else{
      $('.availablities .applying_days').append('<span>'+apply_enter_number+' Days</span><input style="display: none;" name="num_of_days" id="num_of_days" type="text" value="'+apply_enter_number+'">')
    }
  }
}

function SessionAssemble(){
  let session_sender = 0
  let onchange_from_session = parseFloat($('.session_block [name="from_session_type"]').val())
  let onchange_to_session = parseFloat($('.session_block [name="to_session_type"]').val())

  let disabled_to_session = $('.session_block select[name="to_session_type"]:disabled')
  if(disabled_to_session.length == 1){
    session_sender = onchange_from_session+1
  }else{
    session_sender = onchange_from_session+onchange_to_session
  }
  return session_sender
}

function LeaveRestriction(SelectedLeaveCount){
  let restricted_key = leave_storage[1]['Balance'];
  if(CurrentSelected_LeaveType == 'SL'){
    if(SelectedLeaveCount > 3){
      $('#alert_modal .alert_modal_text').text("Not allowed to apply more than 3 days.");
      $('#alert_modal').fadeIn(1000);
    }else if(parseFloat(restricted_key['sl']) < SelectedLeaveCount){
      $('#alert_modal .alert_modal_text').text("Apply the leave based on your available balance.");
      $('#alert_modal').fadeIn(1000);
    }
  }else if(CurrentSelected_LeaveType == 'CL'){
    if(SelectedLeaveCount > 3){
      $('#alert_modal .alert_modal_text').text("Not allowed to apply more than 3 days.");
      $('#alert_modal').fadeIn(1000);
    }else if(parseFloat(restricted_key['cl']) < SelectedLeaveCount){
      $('#alert_modal .alert_modal_text').text("Apply the leave based on your available balance.");
      $('#alert_modal').fadeIn(1000);
    }
  }
}

function DateDiffernce(from_date, to_date){
  const date1 = new Date(from_date);
  const date2 = new Date(to_date);
  const diffTime = Math.abs(date2 - date1);
  const diffDays = Math.ceil(diffTime/(1000*60*60*24));
  return diffDays
}

/****************************** On - From Date Change ******************************/
$('.leave_date_and_session input#fromDate').on('change', function(){
  applydays_for_date = 0
  let from_selected_from_date = $(this).val()
  let from_selected_to_date = $('.leave_date_and_session input#toDate').val()
  let fromchange_days = DateDiffernce(from_selected_from_date, from_selected_to_date)
  applydays_for_date = applydays_for_date+fromchange_days
  console.log(from_selected_from_date, from_selected_to_date)
  console.log(applydays_for_date)
  if(from_selected_from_date == from_selected_to_date){
    $('.session_block [name="from_session_type"]').val("1.0").change();
    $('.session_block [name="to_session_type"]').val("1.0").change();
    $('.session_block select[name="to_session_type"]').prop("disabled", true);
  }else{
    $('.session_block select[name="to_session_type"]').prop("disabled", false);
  }
  final_applying_days = (applydays_for_date+SessionAssemble())-1
  ApplyingDaysForamtion(final_applying_days)
  LeaveRestriction(final_applying_days)
});

/****************************** On - To Date Change ******************************/
$('.leave_date_and_session input#toDate').on('change', function(){
  applydays_for_date = 0
  let to_selected_to_date = $(this).val()
  let to_selected_from_date = $('.leave_date_and_session input#fromDate').val()
  let tochange_days = DateDiffernce(to_selected_from_date, to_selected_to_date)
  applydays_for_date = applydays_for_date+tochange_days
  if(to_selected_from_date == to_selected_to_date){
    $('.session_block [name="from_session_type"]').val("1.0").change();
    $('.session_block [name="to_session_type"]').val("1.0").change();
    $('.session_block select[name="to_session_type"]').prop("disabled", true);
  }else{
    $('.session_block select[name="to_session_type"]').prop("disabled", false);
  }
  final_applying_days = (applydays_for_date+SessionAssemble())-1
  ApplyingDaysForamtion(final_applying_days)
  LeaveRestriction(final_applying_days)
});

/****************************** On - From Session Change ******************************/
$('.session_block [name="from_session_type"]').on('change', function(){
  let from_session_value = $(this).val()
  let sessionchange_fromdate = $('.leave_date_and_session input#fromDate').val()
  let sessionchange_todate = $('.leave_date_and_session input#toDate').val()

  $(this).find("option:first-child").hide();
  
  if(sessionchange_fromdate == sessionchange_todate){
    $(this).find("option:first-child").hide();
    if(from_session_value == "0.5"){
      $('.session_block [name="to_session_type"]').val("0.5").change();
    }else if(from_session_value == "1.0"){
      $('.session_block [name="to_session_type"]').val("1.0").change();
    }
  }
  final_applying_days = (applydays_for_date+SessionAssemble())-1
  ApplyingDaysForamtion(final_applying_days)
  LeaveRestriction(final_applying_days)
});

/****************************** On - From Session Change ******************************/
$('.session_block [name="to_session_type"]').on('change', function(){
  let to_session_value = $(this).val()
  let sessionchange_fromdate = $('.leave_date_and_session input#fromDate').val()
  let sessionchange_todate = $('.leave_date_and_session input#toDate').val()
  $(this).find("option:first-child").hide();
  final_applying_days = (applydays_for_date+SessionAssemble())-1
  ApplyingDaysForamtion(final_applying_days)
  LeaveRestriction(final_applying_days)
});


/* ################################################################ Leave Status ################################################################ */
/* #################################### on status combo #################################### */
function status_and_approval_color(){
  $('.leave_status_table tbody tr td[value]').each(function(){
      let status_text = $(this).attr('value');
      if(status_text == "Approved"){
        $(this).css({'background': '#dbf8e9', 'color': '#41966d'})
      }else if(status_text == "Pending"){
        $(this).css({'background': '#fdf5e4', 'color': '#d6a867'})
      }else if(status_text == "Rejected"){
        $(this).css({'background': '#fde9eb', 'color': '#e27b8a'})
      }
  });
}

$('.leave_status_table tbody tr td[value]').on('click',function(){
  let table_col_headers = []
  let table_values = []
  let selected_row_values = []
  $('.leave_status_table tr th').each(function(){
    table_col_headers.push($(this).text())
  });
  $(this).parent().find('td').each(function(){
    if($(this).find('b').length == 1){
      table_values.push($(this).find('.reason_tooltiptext').text())
    }else{
      table_values.push($(this).text())
    }
  });

  if(table_col_headers.length == table_values.length){
    for (var i = 0; i < table_col_headers.length; i++){
      if(['Approved', 'Pending', 'Rejected'].includes(table_values[i])){
        if(table_values[i] == "Approved"){
          selected_row_values.push('<li class="col-md-2"><b>'+table_col_headers[i]+'</b><span style="color:Green">'+table_values[i]+'</span></li><input type="hidden" name="'+table_col_headers[i].toLowerCase().replace(' ','_')+'" value="'+table_values[i]+'">');
        }else if(table_values[i] == "Pending"){
          selected_row_values.push('<li class="col-md-2"><b>'+table_col_headers[i]+'</b><span style="color:Orange">'+table_values[i]+'</span></li><input type="hidden" name="'+table_col_headers[i].toLowerCase().replace(' ','_')+'" value="'+table_values[i]+'">');
        }else if(table_values[i] == "Rejected"){
          selected_row_values.push('<li class="col-md-2"><b>'+table_col_headers[i]+'</b><span style="color:Red">'+table_values[i]+'</span></li><input type="hidden" name="'+table_col_headers[i].toLowerCase().replace(' ','_')+'" value="'+table_values[i]+'">');
        }
      }else{
        selected_row_values.push('<li class="col-md-2"><b>'+table_col_headers[i]+'</b><span>'+table_values[i]+'</span></li><input type="hidden" name="'+table_col_headers[i].toLowerCase().replace(' ','_')+'" value="'+table_values[i]+'">');
      }
    }
  }

  if ($("form.confirm_form ul li").length == 0){
    $("form.confirm_form ul").append(selected_row_values);
  }else{
    $("form.confirm_form ul li").remove();
    $("form.confirm_form ul input").remove();
    $("form.confirm_form ul").append(selected_row_values);
  }

  let mode_change = $(this).text()
  if(['ADMIN','TA'].includes(data_storage['emp_type'])){
    $('#approve_confirm').css('display','block');
  }else if(['TMR', 'TM', "TBHR", 'TBH'].includes(data_storage['emp_type'])){
    if(data_storage['emp_id'] == leave_storage[1]['reporting1']['emp_id2'] || data_storage['emp_id'] == leave_storage[1]['reporting2']['emp_id']){
      if (mode_change == 'Pending'){
        $('#approve_confirm').css('display','block');
      }
    }
  }

});

/* #################################### Confirmation Module */
function approve_confirm_validation(){
  let confirm_code = $('#approve_confirm button[value="approved"]').val()
  if(confirm_code == 'approved'){
    $('#approve_confirm form').append('<input type="hidden" name="final_confirm" value="Approved">')
  }
}

function reject_confirm_validation(){
  let confirm_code = $('#approve_confirm button[value="rejected"]').val()
  if(confirm_code == 'rejected'){
    $('#approve_confirm form').append('<input type="hidden" name="final_confirm" value="Rejected">')
  }
}
/* ################################################################ Leave Status ################################################################ */

// /* ################################################################ Clear Cache Contents ################################################################ */
function availablities_clear(){
  $('.availablities .applying_days span').text('')
  $('.availablities .permission_hours span').text('')
  $('.availablities .balance span').text('')
}

function DateAndSession_Clear(){
  // $('#leave_apply_tab #fromDate').val('')
  // $('#leave_apply_tab #toDate').val('')
  $('.session_block [name="from_session_type"]').val('').change()
  $('.session_block [name="to_session_type"]').val('').change()

  $('#leave_apply_tab #permDate').val('')
  $('#leave_apply_tab [name="perm_hours_type"]').val('').change()

  $('#leave_apply_tab #odDate').val('')
  $('.session_block select[name="to_session_type"]').prop("disabled", false);
}

function cancel_execution(){
  if($('.leave_application .apply_for select').val() != ''){
    $('.leave_application .apply_for select').val('');
    $('.leave_application .for_leave_application').css('display', 'none')
    $('.leave_application .for_permission_application').css('display', 'none')
    $('.leave_application .for_od_application').css('display', 'none')
  }
  DateAndSession_Clear()
  availablities_clear()
  $('.availablities').css('display', 'none')
  $('#leave_reason').val('');
}
// /* ################################################################ Clear Cache Contents ################################################################ */