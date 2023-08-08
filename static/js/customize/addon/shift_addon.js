var data_storage = JSON.parse(my_storage);
var shift_storage = JSON.parse(workshift_store);

$(document).ready(function($){
	$('button.shift_show_tab_link').css({'color':'#fff','background-color': '#00b1b3', 'font-size': '14px', 'font-weight': '600'})
    // $('button.shift_assign_tab_link').css({'color':'#fff','background-color': '#00b1b3', 'font-size': '14px', 'font-weight': '600'})
    // $('button.newuser_tab_link').css({'color':'#fff','background-color': '#00b1b3', 'font-size': '14px', 'font-weight': '600'})
    
    $('#shift_assign_tab').css('display','none');
    $('#shift_show_tab').css('display','block');
    $('#newuser_station_tab').css('display','none');
});

/* ################################################################ Tab Movement ################################################################ */
function moveReport(evt, tabname){
    var iter, tabcontent, tablinks;
    if(tabname == 'addon_shift_assign'){
        $('#shift_assign_tab').css('display','block');
        $('#shift_show_tab').css('display','none');
        $('#newuser_station_tab').css('display','none');
        $('button.shift_assign_tab_link').css({'color':'#fff','background-color': '#00b1b3', 'font-size': '14px', 'font-weight': '600'})
        $('button.shift_show_tab_link').css({'color':'#000','background-color': 'transparent', 'font-size': '13px', 'font-weight': '600'})
        $('button.newuser_tab_link').css({'color':'#000','background-color': 'transparent', 'font-size': '13px', 'font-weight': '600'})
    }else if(tabname == 'addon_shift_show'){
        $('#shift_assign_tab').css('display','none');
        $('#shift_show_tab').css('display','block');
        $('#newuser_station_tab').css('display','none');
        $('button.shift_assign_tab_link').css({'color':'#000','background-color': 'transparent', 'font-size': '13px', 'font-weight': '600'})
        $('button.shift_show_tab_link').css({'color':'#fff','background-color': '#00b1b3', 'font-size': '14px', 'font-weight': '600'})
        $('button.newuser_tab_link').css({'color':'#000','background-color': 'transparent', 'font-size': '13px', 'font-weight': '600'})
    }else if(tabname == 'addon_newuser'){
        $('#shift_assign_tab').css('display','none');
        $('#shift_show_tab').css('display','none');
        $('#newuser_station_tab').css('display','block');
        $('button.shift_assign_tab_link').css({'color':'#000','background-color': 'transparent', 'font-size': '13px', 'font-weight': '600'})
        $('button.shift_show_tab_link').css({'color':'#000','background-color': 'transparent', 'font-size': '13px', 'font-weight': '600'})
        $('button.newuser_tab_link').css({'color':'#fff','background-color': '#00b1b3', 'font-size': '14px', 'font-weight': '600'})
    }
}
/* ################################################################ Tab Movement ################################################################ */


/* @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ - Shift New Users Assign - @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ */
// select & deselect users
$('#newuser_station_tab .multiselect_content label').on('click',function(){
	let current_select_val = $(this).parent().find('input').val()
	if (current_select_val == 'all'){
		if($(this).parent().find('input').is(':checked') == true){
			$('#newuser_station_tab .multiselect_content input').prop('checked', false)
			$(this).parent().find('input').prop('checked',true)	
		}else{
			$('#newuser_station_tab .multiselect_content input').prop('checked', true)
			$(this).parent().find('input').prop('checked',false)
		}
	}
});
// Dropdown select users
$('#newuser_station_tab button.multiselect_btn').on('click', function(){
	let staged_click = $('#newuser_station_tab .multiselect_content.d-none').length
	if (staged_click == 1){
		$('#newuser_station_tab .multiselect_content').removeClass("d-none")
		$(this).text('Select & Hide Users')
	}else if (staged_click == 0){
		$('#newuser_station_tab .multiselect_content').addClass("d-none")
		$(this).text('Show Users')
	}	
});
function NewUser_Validation(){
    let check_list = [];
    let error_data = ""
    let newusercheck_valid_data = $('#newuser_station_tab .multiselect_content input:checked').length
    if (newusercheck_valid_data == 0){
        error_data = "Please select the users.."
        check_list.push(error_data);
    }else{
    	let newprojectselect_valid_data = $('#newuser_station_tab #newuser_selection_shift select[name="newuser_project"]').val();
    	if (newprojectselect_valid_data == ''){
    		error_data = "Please select the project you map.."
        	check_list.push(error_data);
        }else{
        	let newshiftselect_valid_data = $('#newuser_station_tab #newuser_selection_shift select[name="newuser_selection_shift"]').val();
	    	if (newshiftselect_valid_data == ''){
	    		error_data = "Please select the shift you assign.."
	        	check_list.push(error_data);
	        }
        }
    }
    return check_list;
}
function NewUser_finalSubmision(event){
    let newuser_triger = NewUser_Validation()
    if (newuser_triger.length != 0){
        $('#newuser_station_tab .error_block').css({'display':'block', 'text-align': 'center'})
        $('#newuser_station_tab .error_block p').text(newuser_triger[0])
        event.preventDefault();
    }
}
function NewUser_ClearCache(event){
	$('#newuser_station_tab .multiselect_content input').prop('checked', false)
	$('#newuser_station_tab .multiselect_content').addClass("d-none")	
	$('#newuser_station_tab button.multiselect_btn').text('Show Users')
	$('#newuser_station_tab #newuser_selection_shift select[name="newuser_project"]').val('')
	$('#newuser_station_tab #newuser_selection_shift select[name="newuser_selection_shift"]').val('')
	$('#newuser_station_tab .error_block p').text('')
    $('#newuser_station_tab .error_block').css('display','none')
}

/* @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ - Shift Assign Block - @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ */
$('#shift_assign_tab #project_head select[name="shift_timing_id"]').on('change',function(){
	let common_assign_shift = $(this).val();
	console.log(common_assign_shift)
	$('#shift_assign_tab .inner_user_block select[name="shift_timing_for_users"]').val(common_assign_shift);
	$('#shift_assign_tab .inner_user_block select[name="shift_timing_for_users"]').prop('disabled',true);
});

$('#shift_assign_tab #project_head a').on('click',function(){
	let show_usersblock = $('#shift_assign_tab [id*="connect_collapse"].show').length
	// Working in reverse logic
	if (show_usersblock == 1){
		$('.inner_user_block select[name="shift_timing_for_users"]').prop('disabled',true)
		$(this).text('Users')
		$('#shift_assign_tab #project_head select[name="shift_timing_id"]').prop('disabled',false)
		$(this).css({'background':'#457b9d', 'color': '#fff', 'padding': '6px'})
	}else{
		$('.inner_user_block select[name="shift_timing_for_users"]').prop('disabled',false)
		$(this).text('Hide')
		$(this).css({'background':'#e5e5e5', 'color': '#000', 'padding': '7px'})
		$('#shift_assign_tab #project_head select[name="shift_timing_id"]').prop('disabled',true)
	}
});
function ShiftAssign_Validation(){
    let check_list = [];
    let error_data = ""
    let common_shift_element = $('#shift_assign_tab #project_head select[name="shift_timing_id"]')
    if (common_shift_element.is(':disabled')){
		console.log('Set')    	
    }else{
	    let assign_shift_valid = $('#shift_assign_tab #project_head select[name="shift_timing_id"]').val()
	    if (assign_shift_valid == ''){
			var check_val = 0;
			$(".inner_user_block input").each(function(){
				let inner_val = $(this).val();
				if (inner_val.includes("U")){
					check_val = 1;
					return false;
				}
			});
			if (check_val != 1){
				error_data = "Please select the project shift.."
				check_list.push(error_data);
			}
	    }
    }
    return check_list;
}
function ShiftAssing_FinalSubmission(event){
    let newuser_triger = ShiftAssign_Validation()
    if (newuser_triger.length != 0){
        $('#shift_assign_tab .error_block').css({'display':'block', 'text-align': 'center'})
        $('#shift_assign_tab .error_block p').text(newuser_triger[0])
        event.preventDefault();
    }
}

function BackToShifts(){
	$('button.shift_show_tab_link').prop('disabled',false)
	$('button.shift_assign_tab_link').prop('hidden',true)
	$('button.newuser_tab_link').prop('hidden',true)
    $('#addon_creation').css('display','none');
    $('#shift_assign_tab').css('display','none');
    $('#shift_show_tab').css('display','block');
    $('#newuser_station_tab').css('display','none');
    $('button.process_tab_link').css({'color':'#000','background-color': 'transparent', 'font-size': '13px', 'font-weight': '600'})
    $('button.shift_assign_tab_link').css({'color':'#000','background-color': 'transparent', 'font-size': '13px', 'font-weight': '600'})
    $('button.shift_show_tab_link').css({'color':'#fff','background-color': '#00b1b3', 'font-size': '14px', 'font-weight': '600'})
    $('button.newuser_tab_link').css({'color':'#000','background-color': 'transparent', 'font-size': '13px', 'font-weight': '600'})
}


/* @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ - Shift Show Block - @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ */
// onproject change & filter
$('#shift_show_tab .shift_project_selection select[name="show_project"]').on('change', function(){
	let show_project_id = $(this).val()
	if(show_project_id != ''){
		$('#shift_show_tab ul.project_segment li.show_project_lister').each(function(){
			if ($(this).attr('data-id') == show_project_id){
				$(this).css('display', 'flex');
			}else{
				$(this).css('display', 'none');
			}
		});		
	}else{
		$('#shift_show_tab ul.project_segment li.show_project_lister').each(function(){
			$(this).css('display', 'flex');
		});
	}
});

// Project List Manitenance work
$('#shift_show_tab .project_segment li.show_project_lister').each(function(){
	let visible_prject_name = $(this).attr('data-attribute')
	let visible_prject_id = $(this).attr('data-id')

	let colleced_shift_list = []
	$(this).find('.inner_user_block tbody tr').each(function(){
		let td_data = $(this).find('td[shift-data]').text();
		if (colleced_shift_list.includes(td_data)== false){
			colleced_shift_list.push(td_data)
		}
	});
	let unique_shift_list = []
	console.log(colleced_shift_list);
	$($.unique(colleced_shift_list)).each(function(indd, elem){unique_shift_list.push('<li bro-code="'+(parseInt(indd)+1)+'">'+elem+'</li>')});
	let viewall_content = '<li bro-code="0" style="width: 5%;">All</li>'
	$(this).find('.cardtop_shiftnumber_block ul.shift_eleven').append(viewall_content+unique_shift_list.join(""))

	// Users select & Set
	$(this).find('.cardtop_showall_block a').on('click',function(){
		let show_usersblock = $('#shift_show_tab [id="'+visible_prject_name+' store_collapse"].show').length
		// Working in reverse logic
		if (show_usersblock == 1){
			$(this).text('Show Users')
			$(this).find('.cardtop_shiftnumber_block ul li').each(function(){
				$(this).css({'background-color':'#a8dadc50', 'color': '#fff'})
				$('#shift_show_tab [data-id="'+visible_prject_id+'"] .inner_user_block tbody tr').each(function(){$(this).show()});
			});
			$(this).css({'color': '#fff'}).parent().css({'background':'#457b9d'})
		}else{
			$(this).text('Hide Users')
			$(this).css({'color': '#000'}).parent().css({'background':'#e5e5e5'})
		}
	});

	// avail shifts filter execution
	$(this).find('.cardtop_shiftnumber_block ul li').on('click',function(){
		let brocode = $(this).attr('bro-code')
		$('#shift_show_tab [data-id="'+visible_prject_id+'"] .cardtop_shiftnumber_block ul li').each(function(ind, ele){
			if (brocode == (ind).toString()){
				$(this).css({'background-color':'#00b1b3', 'color': '#fff'})
				if (ind == 0){
					$('#shift_show_tab [data-id="'+visible_prject_id+'"] .inner_user_block tbody tr').each(function(){
						$(this).show()
					});
				}else{
					let filtered_shift = $(this).text()
					$('#shift_show_tab [data-id="'+visible_prject_id+'"] .inner_user_block tbody tr').each(function(){
						let default_shift = $(this).find('td[shift-data]').text()
						if(filtered_shift == default_shift){$(this).show()}else{$(this).hide()}
					});
				}
			}else{
				$(this).css({'background-color':'#b6b9b950', 'color': '#000'})
			}
		});
	});
});

// avail shifts filter execution
// $('#shift_show_tab .cardtop_shiftnumber_block ul li').on('click',function(){
// 	let brocode = $(this).attr('bro-code')
// 	console.log(brocode)

// 	$('#shift_show_tab .cardtop_shiftnumber_block ul li').each(function(ind, ele){
// 		if (brocode == (ind+1).toString()){
// 			$(this).css({'background-color':'#00b1b3', 'color': '#fff'})
// 			let filtered_shift = $(this).text()
// 			$('#shift_show_tab [data-id="36"] .inner_user_block tbody tr').each(function(){
// 				let default_shift = $(this).find('td[shift-data]').text()
// 				if(filtered_shift == default_shift){$(this).show()}else{$(this).hide()}
// 			});
// 		}else{
// 			$(this).css({'background-color':'#b6b9b950', 'color': '#000'})
// 		}
// 	});
// });

function MoveToNew(){ 
	hidden_check = $('button.newuser_tab_link').is(':hidden')
	if(hidden_check == true){
		$('button.newuser_tab_link').prop('hidden',false)
		$('button.shift_show_tab_link').prop('disabled',true)
        
        $('#shift_assign_tab').css('display','none');
        $('#newuser_station_tab').css('display','block');
        $('#shift_show_tab').css('display','none');
	    $('#addon_creation').css('display','none');
        
        $('button.process_tab_link').css({'color':'#000','background-color': 'transparent', 'font-size': '13px', 'font-weight': '600'})
        $('button.shift_show_tab_link').css({'color':'#000','background-color': 'transparent', 'font-size': '13px', 'font-weight': '600'})
        $('button.shift_assign_tab_link').css({'color':'#000','background-color': 'transparent', 'font-size': '13px', 'font-weight': '600'})
        $('button.newuser_tab_link').css({'color':'#fff','background-color': '#00b1b3', 'font-size': '14px', 'font-weight': '600'})
	}else{
		$('button.newuser_tab_link').prop('hidden',true)
		$('button.shift_show_tab_link').prop('disabled',false)
	    
	    $('#shift_show_tab').css('display','block');
	    $('#shift_assign_tab').css('display','none');
	    $('#newuser_station_tab').css('display','none');
	    $('#addon_creation').css('display','none');

	    $('button.process_tab_link').css({'color':'#000','background-color': 'transparent', 'font-size': '13px', 'font-weight': '600'})
        $('button.shift_assign_tab_link').css({'color':'#000','background-color': 'transparent', 'font-size': '13px', 'font-weight': '600'})
        $('button.shift_show_tab_link').css({'color':'#fff','background-color': '#00b1b3', 'font-size': '14px', 'font-weight': '600'})
        $('button.newuser_tab_link').css({'color':'#000','background-color': 'transparent', 'font-size': '13px', 'font-weight': '600'})
	}
}
function MoveToAssign(project_name){
	let assignrequest_proejctid = project_name.split('|')[0]
	let freezed_shiftassignfinalstring = ''
	let shift_option_list = []
	
	$(shift_storage).each(function(shift_keys, shift_values){
		$(shift_values['all_shifts']).each(function(ii, shift_elements){
			let shiftselection_optionstring = '<option value="N|'+shift_elements['shift_id']+'" data_shift="'+shift_elements['shift_name']+'">'+shift_elements['shift_timings']+' ('+shift_elements['shift_name']+')</option>'
			shift_option_list.push(shiftselection_optionstring)
		});
		let common_projectselectstring = '<option value="">Assign Shift For Project</option>'+shift_option_list.join("")
		let singleuser_selectstring = '<option value="">Select Shift</option>'+shift_option_list.join("")
		// for provide shift option to all users
		$(shift_values['projects']).each(function(ii, shift_projects){
			if(assignrequest_proejctid == shift_projects['project_id']){
				let tr_list = []
				$(shift_projects['users']).each(function(jj, uds){
					let final_trstring = '<tr data-row="'+(jj+1)+'"><td>'+uds['wiss_employee_id']+'</td><td>'+uds['employee_name']+'</td><td>'+uds['designation']+'</td><td>'+uds['shift_name']+'</td><td>'+uds['shift_timings']+'</td><td><select name="shift_timing_for_users_'+uds['employee_id']+'_'+uds['designation_id']+'">'+singleuser_selectstring+'</select></td></tr>'
					tr_list.push(final_trstring)
				});
				let assignproject_name = shift_projects['project_name']
				let assignproject_id = shift_projects['project_id']
				let projectmanagerid = shift_projects['manager_id']
				let projectheadid = shift_projects['head_id']
				let projectuserscount = shift_projects['users'].length
				let assingedproject_finalstring = '<li data-attribute="'+assignproject_name+'"><div class="card"><span class="project_counter">'+projectuserscount+'</span><div class="card-header" role="tab" id="project_head"><h5 class="collect_assign_project">'+assignproject_name+'</h5><input type="text" name="assign_project_id" value="'+assignproject_id+'" hidden><select name="shift_timing_id" class="col-md-4 collapsed">'+common_projectselectstring+'</select><a class="collapsed" data-toggle="collapse" data-parent="#side_menu" href="#'+assignproject_name+' connect_collapse" aria-expanded="false" aria-controls="collapse_1">Users</a><input type="hidden" name="manager_id" value="'+projectmanagerid+'"><input type="hidden" name="head_id" value="'+projectheadid+'"><button class="common_shift_assign" type="submit">Assign</button></div><div id="'+assignproject_name+' connect_collapse" class="collapse" role="tabpanel" aria-labelledby="project_head" data-parent="#side_menu"><div class="card-body"><div class="inner_user_block"><table><thead><th>Employee ID</th><th>Username</th><th>Designation</th><th>Shift Type</th><th>Current Shift</th><th>Shift Timing</th></thead><tbody></tbody>'+tr_list.join("")+'</table></div></div></div></div></li>'
				freezed_shiftassignfinalstring = assingedproject_finalstring
			}
		});	
	}); 

	if($('#shift_assign_tab ul.project_segment li').length == 0){
		$('#shift_assign_tab ul.project_segment').append(freezed_shiftassignfinalstring)
	}else{
		$('#shift_assign_tab ul.project_segment li').remove()
		$('#shift_assign_tab ul.project_segment').append(freezed_shiftassignfinalstring)
	}

	hidden_check = $('button.shift_assign_tab_link').is(':hidden')
	if(hidden_check == true){
		$('button.shift_assign_tab_link').prop('hidden',false)
		$('button.shift_show_tab_link').prop('disabled',true)
	    $('#addon_creation').css('display','none');
        $('#shift_assign_tab').css('display','block');
        $('#shift_show_tab').css('display','none');
        $('#newuser_station_tab').css('display','none');
        $('button.process_tab_link').css({'color':'#000','background-color': 'transparent', 'font-size': '13px', 'font-weight': '600'})
        $('button.shift_assign_tab_link').css({'color':'#fff','background-color': '#00b1b3', 'font-size': '14px', 'font-weight': '600'})
        $('button.shift_show_tab_link').css({'color':'#000','background-color': 'transparent', 'font-size': '13px', 'font-weight': '600'})
        $('button.newuser_tab_link').css({'color':'#000','background-color': 'transparent', 'font-size': '13px', 'font-weight': '600'})
	}else{
		$('button.shift_assign_tab_link').prop('hidden',true)
		$('button.shift_show_tab_link').prop('disabled',false)
	    $('#shift_show_tab').css('display','block');
	    $('#shift_assign_tab').css('display','none');
	    $('#newuser_station_tab').css('display','none');
	    $('#addon_creation').css('display','none');
	    $('button.process_tab_link').css({'color':'#000','background-color': 'transparent', 'font-size': '13px', 'font-weight': '600'})
        $('button.shift_assign_tab_link').css({'color':'#000','background-color': 'transparent', 'font-size': '13px', 'font-weight': '600'})
        $('button.shift_show_tab_link').css({'color':'#fff','background-color': '#00b1b3', 'font-size': '14px', 'font-weight': '600'})
        $('button.newuser_tab_link').css({'color':'#000','background-color': 'transparent', 'font-size': '13px', 'font-weight': '600'})
	}

	$('#shift_assign_tab li tbody tr').each(function(ten, ele){
		let previouscurrent_shift = $(this).find('td:nth-child(4)').text()
		$(this).find('td select option[data_shift="'+previouscurrent_shift+'"]').prop('selected',true)
		$(this).find('td select').on('change', function(){
			let changerowindex = $(this).parent().parent().attr('data-row')
			let selected_val = $(this).val()
			let selected_shift_val = $(this).find('option[value="'+selected_val+'"]').attr('data_shift')

			if (previouscurrent_shift != selected_shift_val){
				if($(this).parent().find('input').length == 0){
					$(this).prop('disabled',true)
					let addedform_value = '<input type="hidden" name="'+$(this).attr('name')+'" value="'+selected_val.replace('N','U')+'">'
					$(this).parent().append(addedform_value)
				}else{
					$(this).prop('disabled',false)
					$(this).parent().find('input').remove();
				}
			}
		});
	});
}

