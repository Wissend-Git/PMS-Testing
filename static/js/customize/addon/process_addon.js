$(document).ready(function($){
    $('[id^="creation_progress"]').css('display', 'none');
    $('.add_more_process, .add_more_tasks').css('display', 'none');
});

var data_storage = JSON.parse(my_storage);

function ul_tag_count(){
    var ul_tag_count = ''
    let ul_list_length = $("#add_more_creation ul").length;
    if (ul_list_length != 0){
        let last_ul_list = $("#add_more_creation ul").last().attr('id').split("_");
        var ul_tag_count = (parseInt(last_ul_list[last_ul_list.length - 1])+1).toString();
    }else{
        var ul_tag_count = $("#add_more_creation ul").length + 2;
    }
    return ul_tag_count
}

$('#addon_project select').on('change', function(){
    let project_selected = $(this).val();
    $('select[name="addon_project"] option[value=""]').css('display', 'none');
    if(project_selected != ''){
        try{
            let project_id = data_storage['employee_projects'][project_selected]['project_id'];
            $("#addon_project_id").val(project_id);
        }catch(error){
            $('select[name="addon_project"] option[value=""]').prop('selected', true);
        }
    }
    display_users_in_dropdown(project_selected)
    clear_cache();
});

$('select[name="addon_type"]').on('change', function(){
    let project_selected_value = $('#addon_project select').val();
    let tag_count = (ul_tag_count()-1).toString();
    if(project_selected_value != ''){
        let addon_val = $(this).val();
        if (addon_val.length == 0){
            $('[id^="creation_progress"]').css('display', 'none');
        }else{
            $('[id^="creation_progress"]').css('display', 'block');
            $('select[name="addon_type"] option[value=""]').css('display', 'none');
            if(addon_val.includes("Task Creation")){
                $('.add_more_tasks').css('display', 'block');
                $('.add_more_process').css('display', 'none');
                $('ul[id^="creation_progress"] [id^="task_creation"]').attr("style","display: block !important");
                $('ul[id^="creation_progress"] [id^="process_creation"]').attr("style","display: none !important");
                $('[id^="process_creation"], [id^="multiuser_container"], [id^="allusers_container"], [class^="mapped_users"]').css('display', 'none');
                $('[id^="creation_progress"] h6').attr("style","display: none !important");
                $('ul[id^="creation_progress"] .clear_btn').attr("style","display: none !important");
            }else{
                $('ul[id^="creation_progress"] [id^="task_creation"]').attr("style","display: none !important");
                $('ul[id^="creation_progress"] [id^="process_creation"]').attr("style","display: inline !important");
                $('li [id^="multiuser_container"]').attr("style","display: inline !important");
                $('li [id^="allusers_container"]').attr("style","display: inline !important");
                $('ul[id^="creation_progress"] .clear_btn').attr("style","display: inline !important; outline: none !important;");
                $('[id^="creation_progress"] h6').attr("style","display: inline !important;");
                display_users_in_dropdown(project_selected_value)
                $('.add_more_tasks').css('display', 'none');
                $('.add_more_process').css('display', 'block');
            }
        }
        $('#addon_error_text').text("");
        clear_cache();
        $('#add_more_creation [id^="creation_progress"]').remove();
    }else{
        $('#addon_error_text').text("Please select the project");
    }
});

function display_users_in_dropdown(project_selected){
    let project_users_list = $('[class*="multiuser_content"] .drop_users');
    $(project_users_list).each(function(){
        let user_project = $(this).find('input').val().split('_')[0]
        let user_name = $(this).find('label')
        let user_id = $(this).find('input').val().split('_')[1]
        if(project_selected == user_project){
            $(this).attr("style","display: block !important");
        }else{
            $(this).attr("style","display: none !important");
        }
    });
}

function remove_entire_additional(){
    $('#add_more_creation').remove();
}

function remove_target_data(remove_element, ul_tag_count){
    $('#add_more_creation ul[id^="creation_progress_'+ul_tag_count+'"]').remove();
};

function multitasks_adding(){
    let validate_output = validate_input();
    let check_list = validate_output[0];
    let tag = validate_output[1];
    let ul_tag_count = validate_output[2];
    if (check_list.length != 0){
        if (check_list[0] == 0){
            $('#addon_error_text').text("Please fill all the inputs");
        }else if(check_list[0] == 1){
            $('#addon_error_text').text("Please select the project");
        }else if(check_list[0] == 3){
            $('#addon_error_text').text("Please enter the new task name");
        }else{
            $('#addon_error_text').text("Please fill all data");
        }
        check_list.pop();
    }else{
        $('#addon_error_text').text("");
        $("#add_more_creation").append(
            '<ul id="creation_progress_'+ul_tag_count+'"><li id="task_creation_'+ul_tag_count+'"><label for="task_creation_'+ul_tag_count+'">Task Name</label><input name="task_creation_'+ul_tag_count+'" type="text" placeholder="Type new task here..."><span id="remove_data" onclick="remove_target_data(this,'+ul_tag_count+')">x Remove</span></li></ul>'
        );
    }
}

function multiprocess_adding(){
    let validate_output = validate_input();
    let check_list = validate_output[0];
    let tag = validate_output[1];
    let ul_tag_count = validate_output[2];
    if (check_list.length != 0){
        if (check_list[0] == 0){
            $('#addon_error_text').text("Please fill all the inputs");
        }else if(check_list[0] == 1){
            $('#addon_error_text').text("Please select the project");
        }else if(check_list[0] == 3){
            $('#addon_error_text').text("Please enter the new process name");
        }else if(check_list[0] == 4){
            $('#addon_error_text').text("Please select the options mapping your users!!");
        }else{
            $('#addon_error_text').text("Please fill all data");
        }
        check_list.pop();
    }else{
        $('#addon_error_text').text("");
        let project_selected = $('#addon_project select').val();
        var user_data_list = []
        $.each(data_storage['project_user_data'][project_selected], function(id_, element){
            user_data_list = user_data_list.concat(element);
        });
        let added_data_list = [];
        for (let i=0; i<(user_data_list).length;i++){
            if(project_selected == user_data_list[i][2] && user_data_list[i][5] == 'Active'){
                let label_name = user_data_list[i][0].split('-')[0];
                let drop_users_tag = '<span class="d-block menu-option drop_users"><input name="multiple_user_name_'+ul_tag_count+'_'+i+'" id="multiuser_checkbox_'+ul_tag_count+'_'+project_selected+'_'+user_data_list[i][1]+'_'+i+'" type="checkbox" value="'+project_selected+'_'+user_data_list[i][1]+'" onclick="multiple_users_drop()"><label for="multiuser_checkbox_'+ul_tag_count+'_'+project_selected+'_'+user_data_list[i][1]+'_'+i+'">'+label_name+'</label></span>'
                added_data_list.push(drop_users_tag);
            }
        }
        let added_data = added_data_list.join("");
        $("#add_more_creation").append(
            '<ul id="creation_progress_'+ul_tag_count+'"><li id="process_creation_'+ul_tag_count+'"><label for="process_creation_'+ul_tag_count+'">Process Name</label><input name="process_creation_'+ul_tag_count+'" type="text" placeholder="Type new process here..."></li><li><div id="multiuser_container_'+ul_tag_count+'"><button class="multiuser_btn" type="button" style="outline: none !important;" onclick="users_drop(event)"><i class="fa fa-user-plus"></i>Map Selective Users</button><div class="multiuser_content_'+ul_tag_count+' d-none shadow rounded menu">'+added_data+'</div><div class="d-none" id="multiuserDropdown_'+ul_tag_count+'" onclick="users_drop_hide(event)"></div></div></li><li><h6 style="color: #595959; font-size: 12px; font-weight: 600;">OR</h6></li><li><div id="allusers_container_'+ul_tag_count+'"><button class="alluser_btn" type="button" style="outline: none !important;" onclick="allusers_drop(event)"><i class="fa fa-users"></i>Map All Users</button></div></li><li><div class="mapped_users_'+ul_tag_count+'"><textarea name="final_user_select_'+ul_tag_count+'" type="text" readonly></textarea><input name="final_users_count_'+ul_tag_count+'" type="text" value="0" readonly><button class="clear_btn" type="button" style="outline: none !important;" onclick="clear_data(event)">Clear</button></div></li><span id="remove_data" onclick="remove_target_data(this,'+ul_tag_count+')">X</span></ul>'
        );
    }
}

function validate_input(){
    let ul_list_length = $("#add_more_creation ul").length;
    if (ul_list_length != 0){
        let last_ul_list = $("#add_more_creation ul").last().attr('id').split("_");
        var ul_tag_count = (parseInt(last_ul_list[last_ul_list.length - 1])+1).toString();
    }else{
        var ul_tag_count = $("#add_more_creation ul").length + 2;
    }
    let tag = "creation_progress_"+ul_tag_count;
    var tag_last_count = ul_tag_count-1;
    var tag_count;
    let check_list = [];
    let addon_mode = '';

    if ($('select[name="addon_type"]').val() == "Task Creation"){
        addon_mode = 'task_mode'
        for(tag_count=1; tag_count <= tag_last_count; tag_count++){
            let select_addon_project = $("#addon_project select").val();
            if (select_addon_project.length == 0){
                check_list.push(1);
                return [check_list, tag, ul_tag_count, addon_mode];
            }else{
                let select_addon_type = $("#addon_type select").val();
                if (select_addon_type.length == 0){
                    check_list.push(2);
                    return [check_list, tag, ul_tag_count, addon_mode];
                }else{
                    let new_task_creation = $('[name="'+'task_creation_'+tag_count+'"]').val();
                    if (new_task_creation.length == 0){
                        check_list.push(3);
                        return [check_list, tag, ul_tag_count, addon_mode];
                    }
                }
            }
        }    
    }else{
        addon_mode = 'process_mode'
        for(tag_count=1; tag_count <= tag_last_count; tag_count++){
            let select_addon_project = $("#addon_project select").val();
            if (select_addon_project.length == 0){
                check_list.push(1);
                return [check_list, tag, ul_tag_count, addon_mode];
            }else{
                let select_addon_type = $("#addon_type select").val();
                if (select_addon_type.length == 0){
                    check_list.push(2);
                    return [check_list, tag, ul_tag_count, addon_mode];
                }else{
                    let new_process_creation = $('[name="'+'process_creation_'+tag_count+'"]').val();
                    if (new_process_creation.length == 0){
                        check_list.push(3);
                        return [check_list, tag, ul_tag_count, addon_mode];
                    }else{
                        let selective_users_return = dropdownUsers_checking();
                        let all_users_return = $('#allusers_container_'+tag_count+' input');
                        let values_getter_1 = $('.mapped_users_'+tag_count+' textarea[name="final_user_select_'+tag_count+'"]').val();
                        let values_getter_2 = $('.mapped_users_'+tag_count+' input[name="final_users_count_'+tag_count+'"]').val();
                        if(selective_users_return[0] == 0 && all_users_return.length == 0 && values_getter_1 == '' && values_getter_2 == 0){
                            check_list.push(4);
                            return [check_list, tag, ul_tag_count, addon_mode];
                        }
                    }
                }
            }
        }
    }
    return [check_list, tag, ul_tag_count, addon_mode];
};

function users_drop(event){
    let tag_count = event.target.parentElement.id.split('_')[2];
    event.target.parentElement.children[1].classList.remove("d-none");
    document.getElementById("multiuserDropdown_"+tag_count).classList.remove("d-none");
    $('#addon_error_text').text("");
    $('.mapped_users_'+tag_count).attr("style","display: inline !important");
}

function users_drop_hide(event){
    let tag_count = event.target.parentElement.id.split('_')[2];
    var items = $('.multiuser_content_'+tag_count);
    for (let i = 0; i < items.length; i++){
        items[i].classList.add("d-none");
    }
    $("#multiuserDropdown_"+tag_count).attr('class','d-none')
    // $('.mapped_users_'+tag_count).attr("style","display: none !important");
}

function dropdownUsers_checking(){
    let slected_project = $('#addon_project select').val();
    let tag_count = ul_tag_count();
    let selective_users_input = $('input[id^="multiuser_checkbox_'+(parseInt(tag_count)-1).toString()+'_'+slected_project+'"]');
    let selective_users_value = $('label[for^="multiuser_checkbox_'+(parseInt(tag_count)-1).toString()+'_'+slected_project+'"]');
    if(slected_project != ''){
        let checked_length = []
        $(selective_users_input).each(function(){
            if($(this).is(':checked') == false){checked_length.push('false');}
        });
        if(selective_users_input.length == checked_length.length){
            return [0, slected_project, selective_users_input, selective_users_value];
        }
            return [1, slected_project, selective_users_input, selective_users_value];
    }
}

function allusers_drop(event){
    let slected_project = $('#addon_project select').val();
    let selective_users_return = dropdownUsers_checking();
    let tag_count = event.target.parentElement.id.split('_')[2];
    $('.mapped_users_'+tag_count).attr("style","display: inline !important");
    let final_users = []
    if(slected_project != ''){
        if(selective_users_return[0] == 0){
            if($('#'+event.target.parentElement.id+' input').length == 0){
                $(selective_users_return[3]).each(function(i, ele){
                    unquie_data = unquie_list(final_users, $(this).text())
                    mapped_user_id = $(this).attr('for').split('multiuser_checkbox_'+tag_count)[1].split('_')[2];
                    $('#allusers_container_'+tag_count).append(
                        '<input name="alluser_name_'+tag_count+'_'+(i+1).toString()+'" id="mapped_allusers_'+tag_count+'_'+selective_users_return[1]+'_'+mapped_user_id+'" type="hidden" value="">'
                    );
                    $('input[id^="mapped_allusers_'+tag_count+'_'+selective_users_return[1]+'_'+mapped_user_id+'"]').val(selective_users_return[1]+'_'+mapped_user_id)

                });
                $('.mapped_users_'+tag_count+' textarea[name="final_user_select_'+tag_count+'"]').val(unquie_data)
                $('.mapped_users_'+tag_count+' input[name="final_users_count_'+tag_count+'"]').val(unquie_data.length)
            }
        }else{
            $('#addon_error_text').text("Selective users already mapped");
        }
    }
}

function multiple_users_drop(){
    $('#addon_error_text').text("");
    let tag_count = event.target.parentElement.parentElement.classList[0].split('_')[2];
    let slected_project = $('#addon_project select').val();
    let all_users_return = $('#allusers_container_'+tag_count+' input');
    let selective_users_input = $('input[id^="multiuser_checkbox_'+tag_count+'_'+slected_project+'"]');
    let selective_users_value = $('label[for^="multiuser_checkbox_'+tag_count+'_'+slected_project+'"]');
    let final_users = []
    if(slected_project != ''){
        if(all_users_return.length == 0){
            $(selective_users_input).each(function(){
                if($(this).is(':checked') == true){
                    let selected_user_id = $(this).val().split('_')[1];
                    $(selective_users_value).each(function(){
                        if(selected_user_id == $(this).attr('for').split('multiuser_checkbox_'+tag_count+'_')[1].split('_')[1]){
                            unquie_data = unquie_list(final_users, $(this).text());
                        }
                    });
                }
            });
            $('.mapped_users_'+tag_count+' textarea[name="final_user_select_'+tag_count+'"]').val(unquie_data);
            $('.mapped_users_'+tag_count+' input[name="final_users_count_'+tag_count+'"]').val(unquie_data.length);
            unquie_data.splice(0);
        }else{
            $('#addon_error_text').text("All project users already mapped");
        }
    }
}

function unquie_list(list_name, list_data){
    if(list_name.includes(list_data) == false){
        list_name.push(' '+list_data.trim());
    }
    return list_name
}

function clear_data(){
    tag_count = event.target.parentElement.classList[0].split('_')[2];
    $('#creation_progress_'+tag_count+' #process_creation_'+tag_count+' input').val('');
    $('#creation_progress_'+tag_count+' #task_creation_'+tag_count+' input').val('');
    let map_selective_users = $('#creation_progress_'+tag_count+' #multiuser_container_'+tag_count+' .multiuser_content_'+tag_count+' input');
    let map_all_users = $('#creation_progress_'+tag_count+' #allusers_container_'+tag_count+' input');
    $(map_selective_users).each(function(){
        if($(this).is(':checked') == true){
            $(this).prop('checked', false);
        }
    });
    $(map_all_users).remove();
    $('.mapped_users_'+tag_count+' textarea[name="final_user_select_'+tag_count+'"]').val('');
    $('.mapped_users_'+tag_count+' input[name="final_users_count_'+tag_count+'"]').val(0);
    $('#addon_error_text').text("");
    $('.mapped_users_'+tag_count).attr("style","display: none !important");
}

function clear_cache(){
    $('#add_more_creation [id^="creation_progress"]').remove();
    let tag_count = ul_tag_count()-1;
    $('#creation_progress_'+tag_count+' #process_creation_'+tag_count+' input').val('');
    $('#creation_progress_'+tag_count+' #task_creation_'+tag_count+' input').val('');
    let map_selective_users = $('#creation_progress_'+tag_count+' #multiuser_container_'+tag_count+' .multiuser_content_'+tag_count+' input');
    let map_all_users = $('#creation_progress_'+tag_count+' #allusers_container_'+tag_count+' input');
    $(map_selective_users).each(function(){
        if($(this).is(':checked') == true){
            $(this).prop('checked', false);
        }
    });
    $(map_all_users).remove();
    $('.mapped_users_'+tag_count+' textarea[name="final_user_select_'+tag_count+'"]').val('');
    $('.mapped_users_'+tag_count+' input[name="final_users_count_'+tag_count+'"]').val(0);
    $('#addon_error_text').text("");
    $('.mapped_users_'+tag_count).attr("style","display: none !important");
}

function addon_submit(event){
    let validate_output = validate_input();
    let check_list = validate_output[0];
    if (check_list.length != 0){
        if(validate_output[3] == 'task_mode'){
            if (check_list[0] == 0){
                $('#addon_error_text').text("Please fill all the inputs");
            }else if(check_list[0] == 1){
                $('#addon_error_text').text("Please select the project");
            }else if(check_list[0] == 2){
                $('#addon_error_text').text("Please select the add-on type");
            }else if(check_list[0] == 3){
                $('#addon_error_text').text("Please enter the new task name");
            }else{
                $('#addon_error_text').text("Please fill all data");
            }
            check_list.pop();
        }else{
            if (check_list[0] == 0){
                $('#addon_error_text').text("Please fill all the inputs");
            }else if(check_list[0] == 1){
                $('#addon_error_text').text("Please select the project");
            }else if(check_list[0] == 2){
                $('#addon_error_text').text("Please select the add-on type");
            }else if(check_list[0] == 3){
                $('#addon_error_text').text("Please enter the new process name");
            }else if(check_list[0] == 4){
                $('#addon_error_text').text("Please select the options mapping your users!!");
            }else{
                $('#addon_error_text').text("Please fill all data");
            }
            check_list.pop();
        }
        event.preventDefault();
    }
}