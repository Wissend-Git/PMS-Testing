$(document).ready(function() {
    $('input[id*="_count_"]').on('input', function(){
        let input_id = $(this).attr("id");
        let input_val = $(this).val();
        if (input_val == "" || input_val.includes("-") == true){
            $('#'+input_id).val("");
        }else if(input_val[0] == 0 && input_val.length > 1){
            if ( input_id.includes("hours_count") == false && input_val[0] == 0 && input_val.length > 1){
                $('#'+input_id).val(parseInt(input_val));
            }else if(input_id.includes("hours_count") == true && input_val.includes(".") == false && input_val[0] == 0 && input_val.length > 1){
                $('#'+input_id).val(parseInt(input_val));
            }
        }
    });
    family_buttons_hidden()
    $('.total_hours_count').css('display', 'none');
});

var data_storage = JSON.parse(my_storage);

function auto_filter(id){
    let product_id_list = id.split("_");
    let product_id = product_id_list[product_id_list.length-1];
    let product_type = "product_type_"+product_id;
    $("ul[id^='"+product_type+"'] input[id^='simple_category'],[id^='task_category'],[id^='task_name'],[id^='parentchild_category']").on("change", function(){
        let inp_attr_val = $(this).attr("name");
        let attr_split = inp_attr_val.split("_");
        if (attr_split.length > 4){
            attr_split.pop()
            var inp_attr = attr_split.join("_");
        }else{
            var inp_attr = inp_attr_val;
        }
        let inp_val = $(this).val();
        if (inp_attr.includes("task_name") == true){
            data_id_list = data_storage['task_id_list'];
        }else{
            data_id_list = data_storage['category_id_list'];
        }
        for(let i=0; i < data_id_list.length; i++){
            if (data_id_list[i][0].includes(inp_val) == true){
                $(this).attr("name",inp_attr+"_"+data_id_list[i][1]);
                let input_val = $("input#task_name_"+product_id).val();
                if (input_val.length == 0){
                    let input_attr_data = $("input#task_name_"+product_id).attr('name');
                    let input_attr_split = input_attr_data.split("_");
                    if (input_attr_split.length > 4){
                        input_attr_split.pop()
                        var input_attr_val = input_attr_split.join("_");
                    }else{
                        var input_attr_val = input_attr_data;
                    }
                    for(let j=0; j < data_storage['task_id_list'].length; j++){
                        if (data_storage['task_id_list'][j][0].includes("None") == true){
                            $("input#task_name_"+product_id).attr("name", input_attr_val+"_"+data_storage['task_id_list'][j][1]);
                            break;
                        }
                    }
                }
                break;
            }
        }
    });

    if (id.includes("category")){
        var list_data = data_storage['category_list'];
    }else{
        var list_data = data_storage['task_list'];
    }
    $(id).autocomplete({
        source: list_data,
        minLength:3,
    });
};

//add more product type div
function category_adding(){
    let validate_output = validate_input();
    let check_list = validate_output[0];
    let tag = validate_output[1];
    let ul_tag_count = validate_output[2];
    if (check_list.length != 0){
        if (check_list[0] == 0){
            $('#product_type_error_text').text("Please fill all the inputs");
        }else if(check_list[0] == 1){
            $('#product_type_error_text').text("Please select category name from given category menu");
        }else if(check_list[0] == 2){
            $('#product_type_error_text').text("Please select task name from given task menu");
        }else if(check_list[0] == 3){
            $('#product_type_error_text').text("Please fill hours & minutes");
        }else if(check_list[0] == 4){
            $('#product_type_error_text').text("Please fill achieved count");
        }else{
            $('#product_type_error_text').text("Please select product type");
        }
        check_list.pop();
    }else{
        $('#product_type_error_text').text("");
        $("#add_more_target").append(
            '<ul id="product_type_'+ul_tag_count+'"><li><select id="product_select_'+ul_tag_count+'"  name="product_select_'+ul_tag_count+'" onchange="product_type_select('+"'"+tag+"'"+')"><option value="">Product Type</option><option value="task_'+ul_tag_count+'">Task</option><option value="simple_'+ul_tag_count+'">Simple</option><option value="parentchild_'+ul_tag_count+'">Parent-Child</option></select></li><li id="li_task_'+ul_tag_count+'" class="product_category product_category_inp_'+ul_tag_count+'"><input id="task_category_'+ul_tag_count+'" name="task_category_'+ul_tag_count+'" onkeyup="auto_filter('+"'#task_category_"+ul_tag_count+"'"+')" placeholder="Type & Select Category here..."><input name="task_name_'+ul_tag_count+'" id="task_name_'+ul_tag_count+'" onkeyup="auto_filter('+"'#task_name_"+ul_tag_count+"'"+')"  placeholder="Type & Select Task here..."></li><li id="li_simple_'+ul_tag_count+'" class="product_category product_category_inp_'+ul_tag_count+'"><input id="simple_category_'+ul_tag_count+'" name="simple_category_'+ul_tag_count+'" onkeyup="auto_filter('+"'#simple_category_"+ul_tag_count+"'"+')" placeholder="Type & Select Category here..."></li><li id="li_parentchild_'+ul_tag_count+'" class="product_category product_category_inp_'+ul_tag_count+'"><input id="parentchild_category_'+ul_tag_count+'" name="parentchild_category_'+ul_tag_count+'" onkeyup="auto_filter('+"'#parentchild_category_"+ul_tag_count+"'"+')" placeholder="Type & Select Category here..."></li><li class="product_category_inp_'+ul_tag_count+'"><input type="number" min="0" name="task_count_'+ul_tag_count+'" id="task_count_'+ul_tag_count+'" min="0" oninput="total_count(event)" placeholder="Achieved"><input type="number" min="0" name="parent_count_'+ul_tag_count+'" id="parent_count_'+ul_tag_count+'" min="0" oninput="total_count(event)" placeholder="Parent Count"><input type="number" min="0" oninput="total_count(event)" name="child_count_'+ul_tag_count+'" id="child_count_'+ul_tag_count+'" min="0" placeholder="Child Count"></li><li class="product_category_inp_'+ul_tag_count+'"><input type="number" min="0" id="hours_count_'+ul_tag_count+'" name="hours_count_'+ul_tag_count+'" min="0" placeholder="Hours" oninput="total_hours(event)"><input type="number" min="0" id="minutes_count_'+ul_tag_count+'" name="minutes_count_'+ul_tag_count+'" min="0" placeholder="Minutes" oninput="total_hours(event)"></li><li id="remove_data" onclick="remove_target_data(this)"><p>x Remove</p></li></ul>'
        );
    }
}

//after product type selected
function product_type_select(product_id){
    $('.total_hours_count').css('display', 'block');
    let id_split_list = product_id.split("_");
    let id_num = id_split_list[id_split_list.length-1];
    $('#product_type_error_text').text('');
    let product_type = $('#'+product_id+' select').val();
    $("ul#product_type_"+id_split_list[id_split_list.length-1]+" li input").each(function(){let selected_input_value = $(this).val("");});
    if (product_type.includes("task")){
        $('.product_category_inp_'+id_num+",#task_count_"+id_num).css('display','inline');
        $('#li_simple_'+id_num+', #li_parentchild_'+id_num+', #parent_count_'+id_num+', #child_count_'+id_num).css('display', 'none');
        $('.adding_parent').attr("style", "none");
        $('.adding_child').attr("style", "none");
        $('.adding_both').attr("style", "none");
    }else if(product_type.includes("simple")){
        $('.product_category_inp_'+id_num+', #task_count_'+id_num).css('display','inline');
        $('#li_task_'+id_num+', #li_parentchild_'+id_num+', #parent_count_'+id_num+', #child_count_'+id_num).css('display', 'none');
        $('.adding_parent').attr("style", "none");
        $('.adding_child').attr("style", "none");
        $('.adding_both').attr("style", "none");
    }else{
        $('.product_category_inp_'+id_num+', #parent_count_'+id_num+', #child_count_'+id_num).css('display','inline');
        $('#li_task_'+id_num+', #li_simple_'+id_num+', #task_count_'+id_num).css('display', 'none');
        $('.adding_parent').attr("style", "background-color: #41b29b; color: #fff; border: 0; font-size: 14px; height: 33px; margin-top: -6px; border-radius: 5px; outline: none;");
        $('.adding_child').attr("style", "none");
        $('.adding_both').attr("style", "none");
    }
    $('#'+product_id+' select').css({'background-color':'#daf2f3','color':'#333333', 'border':'1px solid #01cfd3'});
    let doom_list = []
    $('[id^=product_type] li select').each(function(){doom_list.push($(this).val().split('_')[0])});
    if(doom_list.includes("parentchild")){family_buttons_visiblity()}else{family_buttons_hidden()}
    total_count()
}

function validate_input(){
    let ul_list_length = $("#add_more_target ul").length;
    if (ul_list_length != 0){
        let last_ul_list = $("#add_more_target ul").last().attr('id').split("_");
        var ul_tag_count = (parseInt(last_ul_list[last_ul_list.length - 1])+1).toString();
    }else{
        var ul_tag_count = $("#add_more_target ul").length + 2;
    }
    let tag = "product_type_"+ul_tag_count;
    var tag_last_count = ul_tag_count-1;
    var tag_count;
    let check_list = [];
    for(tag_count=1; tag_count <= tag_last_count; tag_count++){
        let select_value = $('#product_select_'+tag_count).val();
        if (select_value.length == 0){
            check_list.push(5);
            return [check_list, tag, ul_tag_count];
        }else{
            $(".project_content #product_type_"+tag_count+" li[style='display: inline;'] input[id$='category_"+tag_count+"'],li[style='display: inline;'] input[id$='name_"+tag_count+"'],li[style='display: inline;'] input[id$='count_"+tag_count+"'][style='display: inline;'],li[style='display: inline;'] input[id$='hours_count_"+tag_count+"']").each(function(){
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
                    let minutes_value = $(this).next().val();
                    if (category_value.length == 0 && minutes_value.length == 0){
                        check_list.push(3);
                        return [check_list, tag, ul_tag_count];
                    }else{
                        let check_hour = parseInt(category_value);
                        let check_minute = parseInt(minutes_value);
                        if (check_hour == 0 && check_minute == 0){
                            console.log("error")
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
    }
    return [check_list, tag, ul_tag_count];
};

function family_buttons_visiblity(){
    $('.family_control label, .note').css('display','block');
    $('.adding_both').css('display','block');
    $('.adding_parent').css('display','block');
    $('.adding_child').css('display','block');
    $('.adding_parent').attr("style", "background-color: #41b29b; color: #fff; border: 0; font-size: 14px; height: 33px; margin-top: -6px; border-radius: 5px; outline: none;");
}

function family_buttons_hidden(){
    $('.family_control label, .note').css('display','none');
    $('.adding_both').css('display','none');
    $('.adding_parent').css('display','none');
    $('.adding_child').css('display','none');
}

function remove_target_data(remove_element){
    $(remove_element).parent().remove();
};

function target_button(event){
    let validate_output = validate_input();
    let check_list = validate_output[0];
    if (check_list.length != 0){
        if (check_list[0] == 0){
            $('#product_type_error_text').text("Please fill all the inputs");
        }else if(check_list[0] == 1){
            $('#product_type_error_text').text("Please select category name from given category menu");
        }else if(check_list[0] == 2){
            $('#product_type_error_text').text("Please select task name from given task menu");
        }else if(check_list[0] == 3){
            $('#product_type_error_text').text("Please fill hours & minutes");
        }else if(check_list[0] == 4){
            $('#product_type_error_text').text("Please fill achieved count");
        }else{
            $('#product_type_error_text').text("Please select product type");
        }
        check_list.pop();
        event.preventDefault();
    }else{
        let target_count = parseInt($('#target_count').val());
        let achieved_count = parseInt($('#achieved_count').val());
        let backlog_count = 0;
        let exceed_count = 0;
        if (target_count > achieved_count){
            backlog_count = target_count - achieved_count;
        }else if(target_count < achieved_count){
            exceed_count = achieved_count - target_count;
        }
        $('#backlog_count').val(backlog_count);
        $('#exceed_count').val(exceed_count);
    }
    let target_val = $("input#target_count").val();
    if (target_val == 0){
        $('#product_type_error_text').text("Please enter target count");
        event.preventDefault();
    }
};

function achieved_count_control(achieved_condition){
    let control_tag = ''
    if(achieved_condition == "task"){
        control_tag = $("input[id^='task_count'],input[id^='parent_count']")
    }else if(achieved_condition == "parent"){
        control_tag = $("input[id^='task_count'],input[id^='parent_count']")
    }else if(achieved_condition == "child"){
        control_tag = $("input[id^='task_count'],input[id^='child_count']")
    }else if(achieved_condition == "both"){
        control_tag = $("input[id^='task_count'],input[id^='parent_count'],input[id^='child_count']")
    }
    let achieved_count_list = [];
    $(control_tag).each(function(){
        let task_count = $(this).val();
        if (task_count != ""){
            achieved_count_list.push(parseInt(task_count));
        }
    });
    let achieved_count = achieved_count_list.reduce((a,b) => a+b, 0);
    $('#achieved_count').val(achieved_count);
}

function common_total_placement(family_mode, total){
    let ul_list = $(".project_content form ul").each(function(){
        let ul_id_list = $(this).attr("id").split("_");
        var ul_tag_count = (parseInt(ul_id_list[ul_id_list.length - 1])).toString();
        let task_count = $("#task_count_"+ul_tag_count).val();
        let parent_count = $("#parent_count_"+ul_tag_count).val();
        let child_count = $("#child_count_"+ul_tag_count).val();
        if(task_count == ""){task_count = 0}
            if(parent_count == ""){parent_count = 0}
                if(child_count == ""){child_count = 0}
        if(family_mode == "task"){
            total = total + parseInt(task_count)+parseInt(parent_count)
        }else if(family_mode == "parent"){
            total = total + parseInt(task_count)+parseInt(parent_count)
        }else if(family_mode == "child"){
            total = total + parseInt(task_count)+parseInt(child_count)
        }else if(family_mode == "both"){
            total = total + parseInt(task_count)+parseInt(parent_count)+parseInt(child_count)
        }
    });
    $("#target_count").val(total)
}


function total_count(){
    var total = 0;
    family_mode = "task"
    common_total_placement(family_mode, total)
    achieved_count_control(family_mode)
}

$('.adding_both').on('click', function(){
    var total = 0;
    family_mode = "both"
    common_total_placement(family_mode, total)
    achieved_count_control(family_mode)
    $('.adding_parent').attr("style", "none");
    $('.adding_child').attr("style", "none");
    $('.adding_both').attr("style", "background-color: #41b29b; color: #fff; border: 0; font-size: 14px; height: 33px; margin-top: -6px; border-radius: 5px; outline: none;");
});

$('.adding_parent').on('click', function(){
    var total = 0;
    family_mode = "parent"
    common_total_placement(family_mode, total)
    achieved_count_control(family_mode)
    $('.adding_parent').attr("style", "background-color: #41b29b; color: #fff; border: 0; font-size: 14px; height: 33px; margin-top: -6px; border-radius: 5px; outline: none;");
    $('.adding_child').attr("style", "none");
    $('.adding_both').attr("style", "none");
});

$('.adding_child').on('click', function(){
    var total = 0;
    family_mode = "child"
    common_total_placement(family_mode, total)
    achieved_count_control(family_mode)
    $('.adding_parent').attr("style", "none");
    $('.adding_child').attr("style", "background-color: #41b29b; color: #fff; border: 0; font-size: 14px; height: 33px; margin-top: -6px; border-radius: 5px; outline: none;");
    $('.adding_both').attr("style", "none");
});


function total_hours(){
    let ul_list = $(".project_content form ul")
    let hours_getter = []
    let mins_getter = []
    $(ul_list).each(function(){
        let ul_id_list = $(this).attr("id").split("_");
        var ul_tag_count = (parseInt(ul_id_list[ul_id_list.length - 1])).toString();
        let hours_count = $("#hours_count_"+ul_tag_count).val();
        let mins_count = $("#minutes_count_"+ul_tag_count).val();
        if(hours_count != "" && mins_count != ""){
            hours_getter.push(parseInt(hours_count))
            mins_getter.push(parseInt(mins_count))
        }else if(hours_count != "" && mins_count == ""){
            hours_getter.push(parseInt(hours_count))
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
    let tribe = final_hrs.toString()+'.'+min_of_mins.toString()
    $('.total_hours_count b').text(tribe)
}   