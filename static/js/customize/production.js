$(document).ready(function() {
    $('.error_block').css('display', 'none')
    $('#production_field_1 span.product_reset').css('right','0px')

    $('.total_hours_count b').text('0.0')
    $('.total_productivity_count b').text('0.0%')
    $('.target_block span').text('0')
    $('.productivity_block span').text('0%')
});

var product_storage = JSON.parse(my_storage);

/* ############################# Get General - Details for Production ############################# */
var active_project_list = []
var active_process_list = []

$.each(product_storage,function(user_key,user_values){
    if(user_key == "employee_projects"){
        $.each(user_values,function(user_project,user_process){
            if(user_process['status'] == "Active"){
                active_project_list.push(user_process['project_id']+"_"+user_project)
            }
            $.each(user_process['process'],function(user_process, user_data_fileds){
            });
        });
    }
});
let project_option_list = []
let process_option_list = []
for (let i=0; i<(active_project_list).length;i++){
    let project_option_tag = '<option value="'+active_project_list[i].split('_')[0]+'" data-value="'+active_project_list[i].split('_')[0]+'">'+active_project_list[i].split('_')[1]+'</option>'
    project_option_list.push(project_option_tag);
}

//enter validation input
function production_field_validation(){
    let check_list = [];
    let error_data = ""
    $('[id^="production_field"]').each(function(field_index, field_values){
        let field_row_number = field_index+1
        let validate_fieldrow = '#production_field_'+field_row_number.toString()
        let input_project_selection = $(validate_fieldrow+' .project_selection select').val();
        if(input_project_selection == ''){
            error_data = [field_row_number, "Please select project.."]
            check_list.push(error_data);
        }else{
            let input_process_selection = $(validate_fieldrow+' .process_selection select').val();
            if(input_process_selection == ''){
                error_data = [field_row_number, "Please select process.."]
                check_list.push(error_data);
            }else{
                let input_task_entry = $(validate_fieldrow+' .task_inputation input[name="task"]').val();
                if(input_task_entry == ''){
                    error_data = [field_row_number, "Please type & select the task.."]
                    check_list.push(error_data);
                }else{
                    let input_achived_entry = $(validate_fieldrow+' .production_inputs_block input[name="achieved"]').val()
                    let input_parent_entry = $(validate_fieldrow+' .production_inputs_block input[name="parent"]').val()
                    let input_child_entry = $(validate_fieldrow+' .production_inputs_block input[name="child"]').val()

                    if(input_achived_entry == ''){
                        if (input_parent_entry == '' && input_child_entry == ''){
                            error_data = [field_row_number, "Please fill the achieved/parent & child count.."]
                            check_list.push(error_data);
                        }
                    }else{
                        let input_hours_entry = $(validate_fieldrow+' .hours_inputs input[name="hours"]').val()
                        let input_mins_entry = $(validate_fieldrow+' .hours_inputs input[name="minutes"]').val()
                        if (input_hours_entry == '' || input_mins_entry == ''){
                            error_data = [field_row_number, "Please fill the hours & minutes.."]
                            check_list.push(error_data);
                        }
                    }
                }
            }
        }
    });
    return check_list;
}

function finalSubmision(event){
    let triger = production_field_validation()
    if (triger.length != 0){
        for (let er=0; er<(triger).length;er++){
            $('.error_block[data-row="'+triger[er][0]+'"]').css('display','block')
            $('.error_block[data-row="'+triger[er][0]+'"] p').text(triger[er][1])
            event.preventDefault();
        }
    }
}

// New Field Adding
function FieldsAdding(event){
    let production_old_number = $(event).parent().parent().attr('data-row')
    let triger = production_field_validation()
    if (triger.length != 0){
        for (let er=0; er<(triger).length;er++){
            $('.error_block[data-row="'+triger[er][0]+'"]').css('display','block')
            $('.error_block[data-row="'+triger[er][0]+'"] p').text(triger[er][1])
            event.preventDefault();
        }
    }else{
        $('.error_block[data-row="'+production_old_number+'"]').css('display','none')
        $('.error_block[data-row="'+production_old_number+'"] p').text('')
        let field_tag_count = parseInt(production_old_number)+1
        let target_calculation = '<input type="number" name="target" value="" hidden><span></span>'
        let productivity_calculation = '<input type="number" name="productivity" value="" hidden><span></span>'
        let project_select_string = '<select name="project" id="project"><option value="" >Select Project</option>"'+project_option_list.join("")+'"</select>'
        let process_select_string = '<select name="process" id="process"><option value="">Select Process</option><option value="testing">Testing</option></select>'
        let added_field = '<div id="production_field_'+field_tag_count+'" class="row production_field" data-row="'+field_tag_count+'"><div class="col-md-12 top_field_row" style="display: inline-flex;"><span class="product_number_count">'+field_tag_count+'</span><span class="product_reset" onclick="ProductionReset(this)"><i class="fa fa-refresh" aria-hidden="true"></i></span><span class="close product_close"  onclick="FieldsRemoving(this)">&times;</span><div class="project_selection"><label for="project">Project<span class="required"> *</span></label>'+project_select_string+'</div><div class="process_selection"><label for="process">Process<span class="required"> *</span></label>'+process_select_string+'</div><div class="task_inputation"><label for="task">Task/Category<span class="required"> *</span></label><input id="task" name="task" placeholder="Type & Select Task here..."></div><div class="production_inputs"><ul id="select_group_type"><li class="custom-checkbox custom-control"><input name="generic_'+field_tag_count+'" type="checkbox" id="generic_'+field_tag_count+'" class="custom-control-input" checked><label class="custom-control-label" for="generic_'+field_tag_count+'">Achieved</label></li><li class="custom-checkbox custom-control"><input name="grouping_'+field_tag_count+'" type="checkbox" id="grouping_'+field_tag_count+'" class="custom-control-input"><label class="custom-control-label" for="grouping_'+field_tag_count+'">Grouping</label></li></ul><div class="production_inputs_block"><input type="number" name="achieved" placeholder="Achieved"><input type="number" name="parent" placeholder="Parent" hidden><input type="number" name="child" placeholder="Child" hidden></div></div><div class="production_hours_input"><label><i class="fa fa-clock-o" aria-hidden="true"></i> Hours<span class="required"> *</span></label><div class="hours_inputs"><input type="number" min="0" max="12" name="hours" placeholder="HH" oninput="TotalHoursAdding(event)"><input type="number" min="0" max="59" name="minutes" placeholder="MM" oninput="TotalHoursAdding(event)"></div></div></div><div class="col-md-12 bottom_field_row" style="display: inline-flex;"><div class="col-md-7 comments_setting"><textarea type="text" name="comments" placeholder="Type your comments here.."></textarea></div><div class="col-md-4 production_setters"><div class="target_block"><label><i class="fa fa-bullseye" aria-hidden="true"></i> Target</label>'+target_calculation+'</div><div class="productivity_block"><label><i class="fa fa-line-chart" aria-hidden="true"></i> Prod (%)</label>'+productivity_calculation+'</div></div></div><div class="col-md-12 error_block" data-row="'+field_tag_count+'"><p></p></div><div class="col-md-12 add_row_block" data-row="'+field_tag_count+'"><button type="button" class="new_production_insert" onclick="FieldsAdding(this)">Add</button></div>'
        $('#new_production_field').append(added_field)
    }
    $('#production_field_'+production_old_number+' .add_row_block').css('display','none');
    $('#production_field_'+production_old_number+' span.product_close').css('display','none')
    $('#production_field_'+production_old_number+' span.product_reset').css('right','0px')
    
}

// Existing Field Removing
function FieldsRemoving(event){
    let field_current_number = $(event).parent().parent().attr('data-row')
    let field_previous_number = field_current_number-1
    $('#production_field_'+field_current_number).remove();
    // Previous Add
    $('#production_field_'+field_previous_number+' .add_row_block').fadeIn(750);
    if (field_previous_number == 1){
        $('#production_field_'+field_previous_number+' span.product_reset').css('right','0px')
        $('#production_field_'+field_previous_number+' span.product_close').css('display','none')
    }else{
        $('#production_field_'+field_previous_number+' span.product_reset').css('right','35px')
        $('#production_field_'+field_previous_number+' span.product_close').css('display','block')
    }
}

// Clear & Reset the Production Fields
function ProductionReset(event){
    let field_row_number = $(event).parent().parent().attr('data-row')
    let reset_fielding = '#production_field_'+field_row_number
    $('.error_block[data-row="'+field_row_number+'"]').css('display','none')
    $('.error_block[data-row="'+field_row_number+'"] p').text('')
    // clear - select fields
    $(reset_fielding+' .project_selection select').val('')
    $(reset_fielding+' .process_selection select').val('')
    $(reset_fielding+' .process_selection select').prop('disabled', true);
    $(reset_fielding+' .task_inputation input[name="task"]').val('')
    // clear - input fields
    let checkup_group = $(reset_fielding+' .production_inputs #select_group_type #generic').is(":checked");
    if(checkup_group == false){
        $(reset_fielding+' .production_inputs #select_group_type #generic').prop('checked', true);
        $(reset_fielding+' .production_inputs #select_group_type #grouping').prop('checked', false);

        $(reset_fielding+' .production_inputs_block input[name="achieved"]').prop('hidden', false);
        $(reset_fielding+' .production_inputs_block input[name="parent"]').prop('hidden', true);
        $(reset_fielding+' .production_inputs_block input[name="child"]').prop('hidden', true);
    }
    $(reset_fielding+' .production_inputs_block input[name="achieved"]').val('')
    $(reset_fielding+' .production_inputs_block input[name="parent"]').val('')
    $(reset_fielding+' .production_inputs_block input[name="child"]').val('')
    // clear - hours fields
    $(reset_fielding+' .hours_inputs input[name="hours"]').val('')
    $(reset_fielding+' .hours_inputs input[name="minutes"]').val('')
    // clear - comments fields
    $(reset_fielding+' .comments_setting textarea').val('')
    $(reset_fielding+' .production_setters input[name="target"]').val('')
    $(reset_fielding+' .production_setters input[name="productivity"]').val('');
}

function TotalHoursAdding(){
    let hours_getter = []
    let mins_getter = []
    $('[id^="production_field"]').each(function(field_index, field_values){
        let production_field_number = field_index+1
        let production_fielding = '#production_field_'+production_field_number.toString()
        let hours_count = $(production_fielding+' .hours_inputs input[name="hours"]').val()
        let mins_count = $(production_fielding+' .hours_inputs input[name="minutes"]').val()
        if (parseInt(mins_count) > 59){
            $(production_fielding+' .hours_inputs input[name="minutes"]').val('0')
            mins_count = '0'
        }
        if (parseInt(hours_count) > 12){
            $(production_fielding+' .hours_inputs input[name="hours"]').val('0')
            hours_count = '0'
        }
        if(hours_count != "" && mins_count != ""){
            hours_getter.push(parseInt(hours_count))
            mins_getter.push(parseInt(mins_count))
        }else if(hours_count != "" && mins_count == ""){
            hours_getter.push(parseInt(hours_count))
            mins_getter.push(0)
        }else if(hours_count == "" && mins_count != ""){
            hours_getter.push(0)
            mins_getter.push(parseInt(hours_count))
        }else{
            hours_getter.push(0)
            mins_getter.push(0)
        }
    });
    let collected_hours = hours_getter.reduce((a,b) => a+b, 0);
    let collected_mins = mins_getter.reduce((a,b) => a+b, 0);
    
    let min_of_hours = Math.floor(collected_mins/60);
    let min_of_mins = (collected_mins%60);
    let final_hrs = collected_hours+min_of_hours

    if(min_of_mins == 60){
        final_hrs = final_hrs+1
        min_of_mins = min_of_mins+0
    }else if(min_of_mins > 0 && min_of_mins < 10){
        min_of_mins = "0"+min_of_mins
    }

    let lock_hours = ''
    let lock_mins = ''
    if (final_hrs.toString() == 'NaN'){lock_hours = '0'}else{lock_hours = final_hrs.toString()}
    if (min_of_mins.toString() == 'NaN'){lock_mins = '0'}else{lock_mins = min_of_mins.toString()}

    let tribe = lock_hours+'.'+lock_mins
    $('.total_hours_count b').text(tribe)
}

/* ############################# IN - Production Box ############################# */
$('[id^="production_field"]').each(function(field_index, field_values){
    let production_field_number = field_index+1
    let production_fielding = '#production_field_'+production_field_number.toString()

    $(production_fielding+' .process_selection select').prop("disabled", true);

    $(production_fielding+' .project_selection select').on('change', function(){
        let _projectname = $(this).val()
        if(_projectname == ''){
            $(production_fielding+' .process_selection select').val('');
            $(production_fielding+' .process_selection select').prop("disabled", true);
        }else{
            $(production_fielding+' .process_selection select').prop("disabled", false);
        }
        $('.error_block[data-row="'+production_field_number+'"]').css('display','none')
        $('.error_block[data-row="'+production_field_number+'"] p').text('')
    });

    $(production_fielding+' .process_selection select').on('change', function(){
        let _projectname = $(this).val()
        if(_projectname == ''){
            $(production_fielding+' .task_inputation input[name="task"]').val('');
            $(production_fielding+' .task_inputation input[name="task"]').prop("disabled", true);
        }else{
            $(production_fielding+' .task_inputation input[name="task"]').prop("disabled", false);
        }
        $('.error_block[data-row="'+production_field_number+'"]').css('display','none')
        $('.error_block[data-row="'+production_field_number+'"] p').text('')
    });

    $(production_fielding+' .task_inputation input').on('change',function(){
        $('.error_block[data-row="'+production_field_number+'"]').css('display','none')
        $('.error_block[data-row="'+production_field_number+'"] p').text('')
    });

    $(production_fielding+' .production_inputs_block input').on('change',function(){
        $('.error_block[data-row="'+production_field_number+'"]').css('display','none')
        $('.error_block[data-row="'+production_field_number+'"] p').text('')
    });


    $(production_fielding+' .hours_inputs input').on('change',function(){
        $('.error_block[data-row="'+production_field_number+'"]').css('display','none')
        $('.error_block[data-row="'+production_field_number+'"] p').text('')
    });
    
    $(production_fielding+' .production_inputs #select_group_type #generic_'+production_field_number).on('click', function(){
        $(production_fielding+' .production_inputs #select_group_type #generic_'+production_field_number).prop('checked', true);
        $(production_fielding+' .production_inputs #select_group_type #grouping_'+production_field_number).prop('checked', false);
        $(production_fielding+' .production_inputs_block input[name="parent"]').val('')
        $(production_fielding+' .production_inputs_block input[name="child"]').val('')
        $(production_fielding+' .production_inputs_block input[name="achieved"]').prop('hidden', false);
        $(production_fielding+' .production_inputs_block input[name="parent"]').prop('hidden', true);
        $(production_fielding+' .production_inputs_block input[name="child"]').prop('hidden', true);
    });

    $(production_fielding+' .production_inputs #select_group_type #grouping_'+production_field_number).on('click', function(){
        $(production_fielding+' .production_inputs #select_group_type #grouping_'+production_field_number).prop('checked', true);
        $(production_fielding+' .production_inputs #select_group_type #generic_'+production_field_number).prop('checked', false);
        $(production_fielding+' .production_inputs_block input[name="achieved"]').val('')
        $(production_fielding+' .production_inputs_block input[name="achieved"]').prop('hidden', true);
        $(production_fielding+' .production_inputs_block input[name="parent"]').prop('hidden', false);
        $(production_fielding+' .production_inputs_block input[name="child"]').prop('hidden', false);
    });
})