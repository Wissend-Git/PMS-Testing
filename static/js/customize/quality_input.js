$(document).ready(function() {

    let check_user_status = $("#quality_check_team").is(":checked");
    if (check_user_status == true){
        $('#quality_check_user').prop('checked', false);
    }else{
        $('#quality_check_team').prop('checked', true);
    }

    let report = $('select[name="report"]').val();
    if (report.length == 0){
        $('[id^="quality_error"]').css('display', 'none');
    }else{
        if (report.includes("file")){
            $("li[id^='user_selected_']").attr("style","display: none !important");
            $("li[id^='file_']").attr("style","display: inline !important");
        }else{
            $("li[id^='user_selected_']").attr("style","display: inline !important");
            $("li[id^='file_']").attr("style","display: none !important");
        }
    }

    // Quality Input Controls
    let selected_project = $('#quality_project select option').val();
    $('[id^="user_selected_"] select[name^="user_selected_"] option').css('display', 'none');
    $('[id^="user_selected_"] select[name^="user_selected_"] option[value^="'+(selected_project)+'"]').css('display', 'block');

    $('[id^="quality_process"] select[name^="quality_process"] option').css('display', 'none');
    $('[id^="quality_process"] select[name^="quality_process"] option[value^="'+(selected_project)+'_"]').css('display', 'block');
    // Quality Input Controls

    if(data_storage['emp_type'] == "TQA"){
        $('select[name="report"] option[value="user"]').css('display', 'none');
        $('select[name*="qc_type_"] option').css('display', 'none');
        $('select[name*="qc_type_"] option[value="Production Audit"]').css('display', 'block');
        $('select[name*="qc_type_"] option[value="QC Audit"]').css('display', 'block');
    }else{
        $('select[name*="qc_type_"] option[value="Production Audit"]').css('display', 'none');
        $('select[name*="qc_type_"] option[value="QC Audit"]').css('display', 'none');
    }
    $('.overall_qc_counts').css('display', 'none')
    
});

var data_storage = JSON.parse(my_storage);

// after quality project user selected
$('#quality_process select').on('change', function(){
    let project_selected = $('#quality_project select').val();
    let process_selected = $(this).val();
    let project_selected_user = $('#project_selected_user select').val();
    if (project_selected_user != ""){
        $('#quality_process option').css('display', 'none');
        $('#quality_process option[value^="'+project_selected_user+'_"], #quality_process option[value="All"]').css('display', 'block');
    }
    if (project_selected != "All"){
        try{
            let project_id = data_storage['employee_projects'][project_selected]['project_id'];
            $("#quality_project_id").val(project_id);
        }catch(error){
            $("#project_selected select option[value='']").prop('selected', true);
        }
    }else{
        $("#quality_project_id").val("All");
    }
    if (process_selected != "All"){
        let process_selected_list = process_selected.split("_");
        let process_selected_data = process_selected_list.pop();
        try{
            let process_id = data_storage['employee_projects'][project_selected]['process'][process_selected_data]['process_id'];
            $("#quality_process_id").val(process_id);
        }catch(error){
            $("#project_selected select option[value='']").prop('selected', true);;
        }
    }else{
        $("#quality_process_id").val("All");
    }
});

// after project vise report selected
$("#quality_check_team").on('click', function(){
    let check_team_status = $("#quality_check_team").is(':checked');
    if (check_team_status == true){
        $('#quality_check_user').prop('checked', false);
    }
    else{
        $('#quality_check_user').prop('checked', true);
    }
});

// after user vise report selected
$("#quality_check_user").on('click', function(){
    let check_team_status = $("#quality_check_user").is(':checked');
    if (check_team_status == true){
        $('#quality_check_team').prop('checked', false);
    }
    else{
        $('#quality_check_team').prop('checked', true);
    }
});

//add more product type div
function quality_adding(){
    let validate_output = validate_input();
    let check_list = validate_output[0];
    let tag = validate_output[1];
    let ul_tag_count = validate_output[2];
    if (check_list.length != 0){
        if (check_list[0] == 0){
            $('#product_type_error_text').text("Please fill all the inputs");
        }else if(check_list[0] == 1){
            $('#product_type_error_text').text("Please select the project");
        }else if(check_list[0] == 2){
            $('#product_type_error_text').text("Please select the process");
        }else if(check_list[0] == 3){
            $('#product_type_error_text').text("Please select the report type");
        }else if(check_list[0] == 4){
            $('#product_type_error_text').text("Please select the qc type");
        }else if(check_list[0] == 5){
            $('#product_type_error_text').text("Please select the user");
        }else if(check_list[0] == 6){
            $('#product_type_error_text').text("Please enter the file name");
        }else if(check_list[0] == 7){
            $('#product_type_error_text').text("Please enter the recieved count");
        }else if(check_list[0] == 8){
            $('#product_type_error_text').text("Please enter the audit count");
        }else if(check_list[0] == 9){
            $('#product_type_error_text').text("Please enter the hours & minutes");
        }else{
            $('#product_type_error_text').text("Please fill all data");
        }
        check_list.pop();
    }else{
        $('#product_type_error_text').text("");
        var user_data_list = []
        $.each(data_storage['selected_project_users'], function(id_, element){
            user_data_list = user_data_list.concat(element);
        });
        let option_data_list = [];
        let project_selected = $("#quality_project select").val();
        for (let i=0; i<(user_data_list).length;i++){
            if (project_selected == user_data_list[i][2] && user_data_list[i][5] == 'Active'){
                let option_tag = "<option value='"+data_storage['project_selected']+"_"+user_data_list[i][1]+"'>"+user_data_list[i][0]+"</option>"
                option_data_list.push(option_tag);
            }
        }
        let option_data = option_data_list.join("");
        $("#add_more_quality").append(
            '<ul id="quality_error_'+ul_tag_count+'"><li><div class="wrap_label"><label for="qc_type_'+ul_tag_count+'">Select Quality Type</label><select name="qc_type_'+ul_tag_count+'"><option value="">Quality Type</option><option value="Floor Audit">Floor Audit</option><option value="Surprise Audit">Surprise Audit</option><option value="Live Audit">Live Audit</option><option value="Prod-Post Audit">Prod-Post Audit</option><option value="Qlty-Post Audit">Qlty-Post Audit</option><option value="Production Audit">Production Audit</option><option value="QC Audit">QC Audit</option></select></div></li><li id="user_selected_'+ul_tag_count+'"><div class="wrap_label"><label for="user_selected_'+ul_tag_count+'">Select User</label><select name="user_selected_'+ul_tag_count+'" id="myFilter"><option value="">User</option>'+option_data+'</select></div></li><li id="file_'+ul_tag_count+'"><div class="wrap_label"><label for="file_'+ul_tag_count+'">File Name</label><input name="file_'+ul_tag_count+'" type="text" placeholder="File Name"></div></li><li><div class="wrap_label_input"><label for="received_'+ul_tag_count+'">Received Count</label><input name="received_'+ul_tag_count+'" type="number" min="0" value="0" oninput="total_recieved_count(event)"></div></li><li><div class="wrap_label_input"><label for="audit_'+ul_tag_count+'">Audit Count</label><input name="audit_'+ul_tag_count+'" type="number" min="0" value="0" oninput="total_audit_count(event)"></div></li><li><div class="wrap_label_input"><label for="missing_'+ul_tag_count+'">Missing Count</label><input name="missing_'+ul_tag_count+'" type="number" min="0" value="0"></div></li><li><div class="wrap_label_input"><label for="incorrect_'+ul_tag_count+'">Incorrect Count</label><input name="incorrect_'+ul_tag_count+'" type="number" min="0" value="0"></div></li><li><div class="wrap_label_input"><label for="spelling_'+ul_tag_count+'">Spelling Count</label><input name="spelling_'+ul_tag_count+'" type="number" min="0" value="0"></div></li><li><div class="wrap_label_input"><label for="normalize_'+ul_tag_count+'">Normalize Count</label><input name="normalize_'+ul_tag_count+'" type="number" min="0" value="0"></div></li><li><div class="wrap_label_input"><label for="hours_'+ul_tag_count+'">Hours</label><input name="hours_'+ul_tag_count+'" type="number" min="0" value="0"></div></li><li><div class="wrap_label_input"><label for="minutes_'+ul_tag_count+'">Minutes</label><input name="minutes_'+ul_tag_count+'" type="number" min="0" value="0"></div></li><li><div class="wrap_label_input quality_comments"><label for="comments_'+ul_tag_count+'">Comments</label><textarea name="comments_'+ul_tag_count+'" id="comments_'+ul_tag_count+'" placeholder="Type here..."></textarea></div></li><li id="remove_data" onclick="remove_target_data(this)"><p>x remove</p></li></ul>'

        );
        let report = $('select[name="report"]').val();
        if (report.length == 0){
            $('[id^="quality_error"]').css('display', 'none');
        }else{
            if (report.includes("file")){
                $("li[id^='user_selected_']").attr("style","display: none !important");
                $("li[id^='file_']").attr("style","display: inline !important");
            }else{
                $("li[id^='user_selected_']").attr("style","display: inline !important");
                $("li[id^='file_']").attr("style","display: none !important");
            }
            if(data_storage['emp_type'] == "TQA"){
                $('select[name="report"] option[value="user"]').css('display', 'none');
                $('select[name*="qc_type_"] option').css('display', 'none');
                $('select[name*="qc_type_"] option[value="Production Audit"]').css('display', 'block');
                $('select[name*="qc_type_"] option[value="QC Audit"]').css('display', 'block');
            }else{
                $('select[name*="qc_type_"] option[value="Production Audit"]').css('display', 'none');
                $('select[name*="qc_type_"] option[value="QC Audit"]').css('display', 'none');
            }
        }
    }
}


function validate_input(){
    let ul_list_length = $("#add_more_quality ul").length;
    if (ul_list_length != 0){
        let last_ul_list = $("#add_more_quality ul").last().attr('id').split("_");
        var ul_tag_count = (parseInt(last_ul_list[last_ul_list.length - 1])+1).toString();
    }else{
        var ul_tag_count = $("#add_more_quality ul").length + 2;
    }
    let tag = "quality_error_"+ul_tag_count;
    var tag_last_count = ul_tag_count-1;
    var tag_count;
    let check_list = [];
    for(tag_count=1; tag_count <= tag_last_count; tag_count++){
        let select_project = $("#quality_project select").val();
        if (select_project.length == 0){
            check_list.push(1);
            return [check_list, tag, ul_tag_count];
        }else{
            let select_process = $("#quality_process select").val();
            if (select_process.length == 0){
                check_list.push(2);
                return [check_list, tag, ul_tag_count];
            }else{
                let select_report = $("select[name='report']").val();
                if (select_report.length == 0){
                    check_list.push(3);
                    return [check_list, tag, ul_tag_count];
                }else{
                    let qc_type = $('[name="'+'qc_type_'+tag_count+'"]').val();
                    if (qc_type.length == 0){
                        check_list.push(4);
                        return [check_list, tag, ul_tag_count];
                    }else{
                        let user_selected = $('[name="'+'user_selected_'+tag_count+'"]').val();
                        if ($("select[name='report']").val() == "user" && user_selected.length == 0){
                            check_list.push(5);
                            return [check_list, tag, ul_tag_count];
                        }else{
                            let file_selected = $('[name="'+'file_'+tag_count+'"]').val();
                            if ($("select[name='report']").val() == "file" && file_selected.length == 0){
                                check_list.push(6);
                                return [check_list, tag, ul_tag_count];
                            }else{
                                let received_count = parseInt($('[name="'+'received_'+tag_count+'"]').val());
                                if (received_count == 0){
                                    check_list.push(7);
                                    return [check_list, tag, ul_tag_count];
                                }else{
                                    let audit_count = parseInt($('[name="'+'audit_'+tag_count+'"]').val());
                                    if (audit_count == 0){
                                        check_list.push(8);
                                        return [check_list, tag, ul_tag_count];
                                    }else{
                                        let hours_count = parseInt($('[name="'+'hours_'+tag_count+'"]').val());
                                        let mins_count = parseInt($('[name="'+'minutes_'+tag_count+'"]').val());
                                        if (hours_count == 0 && mins_count == 0){
                                            check_list.push(9);
                                            return [check_list, tag, ul_tag_count];
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        
        $(".quality_input #quality_error_"+tag_count+" li[style='display: inline;'] input[id$='category_"+tag_count+"'],li[style='display: inline;'] input[id$='name_"+tag_count+"'],li[style='display: inline;'] input[id$='count_"+tag_count+"'][style='display: inline;'],li[style='display: inline;'] input[id$='hours_count_"+tag_count+"']").each(function(){
            let category_id = $(this).attr('id');
            if (category_id.includes("category")){
                let category_value = $(this).val();
                if (data_storage['category_list'].includes(category_value) == false){
                    check_list.push(1);
                    return [check_list, tag, ul_tag_count];
                }
            }else if(category_id.includes("task_name")){
                let category_value = $(this).val();
                if (data_storage['task_list'].includes(category_value) == false){
                    check_list.push(2);
                    return [check_list, tag, ul_tag_count];
                }
            }else if(category_id.includes("hours_")){
                let category_value = $(this).val().trim();
                if (category_value.length == 0){
                    check_list.push(3);
                    return [check_list, tag, ul_tag_count];
                }else{
                    let check_zero = parseFloat(category_value).toString();
                    if (check_zero == 0){
                        check_list.push(3);
                        return [check_list, tag, ul_tag_count];
                    }
                }
            }else if(category_id.includes("_count")){
                let category_value = $(this).val().trim();
                if (category_value.length == 0){
                    check_list.push(4);
                    return [check_list, tag, ul_tag_count];
                }else{
                    let check_zero = parseInt(category_value).toString();
                    if (check_zero == 0){
                        check_list.push(4);
                        return [check_list, tag, ul_tag_count];
                    }
                }
            }
            let input_value = $(this).val().trim();
            if (input_value.length == 0){
                check_list.push(0);
                return [check_list, tag, ul_tag_count];
            }
        });
    }
    return [check_list, tag, ul_tag_count];
};

$('select[name="report"]').on('change', function(){
    let report_val = $(this).val();
    if (report_val.length == 0){
        $('[id^="quality_error"]').css('display', 'none');
    }else{
        $('[id^="quality_error"]').css('display', 'block');
        $('.overall_qc_counts').css('display', 'block')
        if ( report_val.includes("file")){
            $('.quality_input select[name="report"] option[value=""]').css('display', 'none');
            $("li[id^='user_selected_']").attr("style","display: none !important");
            $("li[id^='file_']").attr("style","display: inline !important");
            
        }else{
            let selected_project = $('#quality_project select option').val();
            let user_list = $('[id^="user_selected_"] select[name^="user_selected"]');
            $('.quality_input select[name="report"] option[value=""]').css('display', 'none');
            $("li[id^='user_selected_']").attr("style","display: inline !important");
            $("li[id^='file_']").attr("style","display: none !important");
        }
    }
});

function remove_target_data(remove_element){
    $(remove_element).parent().remove();
};

function quality_submit(event){
    let validate_output = validate_input();
    let check_list = validate_output[0];
    if (check_list.length != 0){
        if (check_list[0] == 0){
            $('#product_type_error_text').text("Please fill all the inputs");
        }else if(check_list[0] == 1){
            $('#product_type_error_text').text("Please select the project");
        }else if(check_list[0] == 2){
            $('#product_type_error_text').text("Please select the process");
        }else if(check_list[0] == 3){
            $('#product_type_error_text').text("Please select the report type");
        }else if(check_list[0] == 4){
            $('#product_type_error_text').text("Please select the qc type");
        }else if(check_list[0] == 5){
            $('#product_type_error_text').text("Please select the user");
        }else if(check_list[0] == 6){
            $('#product_type_error_text').text("Please enter the file name");
        }else if(check_list[0] == 7){
            $('#product_type_error_text').text("Please enter the recieved count");
        }else if(check_list[0] == 8){
            $('#product_type_error_text').text("Please enter the audit count");
        }else if(check_list[0] == 9){
            $('#product_type_error_text').text("Please enter the hours & minutes");
        }else{
            $('#product_type_error_text').text("Please fill all data");
        }
        check_list.pop();
        event.preventDefault();
    }
}

$('[id^="quality_error"] select[name^="qc_type"]').on('change', function(){
    let qc_type = $(this).val();
    if (qc_type != ""){
        $(this).find("option").first().css('display', 'none');
        $('#quality_process option[value^="'+qc_type+'_"], #quality_process option[value="All"]').css('display', 'block');
    }
});

function total_recieved_count(){
    var total = 0
    $(".quality_input form ul").each(function(){
        let ul_id_list = $(this).attr("id");
        if (ul_id_list != undefined){
            ul_id_num = ul_id_list.split("_");
            let ul_tag_count = (parseInt(ul_id_list[ul_id_list.length - 1])).toString();
            let recv_count = $('[name="received_'+ul_tag_count+'"]').val();
            total = total + parseInt(recv_count)
        }
    });
    $(".total_recieved_count").text(total)
}

function total_audit_count(){
    var total = 0
    $(".quality_input form ul").each(function(){
        let ul_id_list = $(this).attr("id");
        if (ul_id_list != undefined){
            ul_id_num = ul_id_list.split("_");
            let ul_tag_count = (parseInt(ul_id_list[ul_id_list.length - 1])).toString();
            let recv_count = $('[name="audit_'+ul_tag_count+'"]').val();
            total = total + parseInt(recv_count)
        }
    });
    $(".total_audited_count").text(total)
}