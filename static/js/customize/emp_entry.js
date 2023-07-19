$(document).ready(function(){
  total_entries()
});

// var data_storage = JSON.parse(my_storage)
// console.log (data_storage['emp_type'])
$('#project_summary_table ul.summary_datas li ul.row_summaries').on('click', function(){
  let selected_project = $(this).attr('data-attribute')
  $("#popup_user_entries").fadeIn(1000);
  $('.popup_entry_list header').css('display', 'none')
  $('.popup_entry_list header[data-value="'+selected_project+'"]').css('display', 'block')
  let total_users = $('.entry_details[data-attribute="'+selected_project+'"] ul.user_columns').length
  $('h3.entry_users_count').text(total_users)
  $('#popup_user_entries .entry_details[data-attribute]').each(function(){
    let loop_project = $(this).attr('data-attribute')
    if(loop_project == selected_project){
      $(this).css('display', 'flex');
    }else{
      $(this).css('display', 'none');
    }
  });
});


function total_entries(){
  let total_projects = $('#project_summary_table ul.summary_datas li.project_selected_rows').length
  let total_employees = []
  let total_actives = []
  let total_deactives = []
  let total_pactives = []
  $('#project_summary_table ul.summary_datas li.project_selected_rows').each(function(indy, ele){
      total_employees.push(parseInt($(ele).find('ul.row_summaries li')[2].innerHTML))
      total_actives.push(parseInt($(ele).find('ul.row_summaries li')[3].innerHTML))
      total_pactives.push(parseInt($(ele).find('ul.row_summaries li')[4].innerHTML))
      total_deactives.push(parseInt($(ele).find('ul.row_summaries li')[5].innerHTML))
  });
  $('span.entries_projects p').text(total_projects)
  $('span.overall_entries p').text(total_employees.reduce((a,b) => a+b, 0))
  $('span.active_entries p').text(total_actives.reduce((a,b) => a+b, 0))
  $('span.partial_entries p').text(total_pactives.reduce((a,b) => a+b, 0))
  $('span.deactive_entries p').text(total_deactives.reduce((a,b) => a+b, 0))
}

$('.popup_entries_close').on('click', function(){
    $("#popup_user_entries").fadeOut(1000);
});