$(document).ready(function(){
    $('#popup_users').attr("style","display: none !important");
    $('#popup_projects').attr("style","display: none !important");

    document.onkeydown = function(e) {
        if(e.keyCode == 27){
            escape_close();
        }
    }
});

var data_storage = JSON.parse(my_storage);

function escape_close(){
    if(['TA', 'ADMIN'].includes(data_storage['emp_type']) == true){
        $("#popup_users").fadeOut(1000);
        if($('ul.js_projects li').length != 0){$("#popup_projects").fadeIn(1000);}
        $('#popup_projects .project_count').attr("style","padding-left: 6px");
    }else{
        $("#popup_users").fadeOut(1000);
        $("#overall_popup_projects").fadeOut(1000);
    }
}

function unquie_list(list_name, list_data){
    if(list_name.includes(list_data) == false){
        list_name.push(list_data.trim());
    }
    return list_name
}

$('.popup_users_close').on('click', function(){
    if(['TA', 'ADMIN'].includes(data_storage['emp_type']) == true){
        $("#popup_users").fadeOut(1000);
        $("#popup_projects").fadeIn(1000);
    }else{
        $("#popup_users").fadeOut(1000);
    }
});

$('.popup_project_close').on('click', function(){
    $("#popup_projects").fadeOut(1000);
});

$('.overall_popup_project_close').on('click', function(){
    $("#overall_popup_projects").fadeOut(1000);
});


/*################################################### User Visiblity Control ###############################################################*/
function user_visibility_control(project_name){
    let heads_dict = {}
    heads_dict['business_head'] = []
    heads_dict['manager'] = []
    heads_dict['lead'] = []
    $('#popup_users .popup_users_content h2.js_project_name').text(project_name)
    $.each(data_storage['employee_projects'][project_name]['process'], function(id_, element){
        business_head = unquie_list(heads_dict['business_head'], element['business_head'])
        manager = unquie_list(heads_dict['manager'], element['manager'])
        lead = unquie_list(heads_dict['lead'], element['lead'])
    });

    var user_data_list = []
    $.each(data_storage['project_user_data'][project_name], function(id_, element){
        user_data_list = user_data_list.concat(element);
    });
    let inactive_leads = []
    $.each(heads_dict['lead'], function(ind_, elemen_){
        for (let i=0; i<(user_data_list).length;i++){
            if(user_data_list[i][0].split('-')[0].trim() == elemen_ && user_data_list[i][5] == "Inactive"){
                inactive_leads.push(user_data_list[i][0].split('-')[0].trim())
            }
        }
    });
    for( var i = 0; i < heads_dict['lead'].length; i++){ 
        if ( heads_dict['lead'][i] == inactive_leads[0]) { 
            heads_dict['lead'].splice(i, 1);
        }
    }
    if(heads_dict['lead'].length == 0){
        heads_dict['lead'].push(heads_dict['manager'][0])
    }

    officals_tag = '<li class="offical_heads"><span>Business Head</span><h6>'+business_head[0]+'</h6></li><li class="offical_heads"><span>Project Manager</span><h6>'+manager[0]+'</h6></li>'
    let lead_users_taglist = []
    let lead_list = []
    if(lead.length == 1){
        let lead_users_tag = '<li class="offical_heads"><span>Current Team Lead</span><h6>'+lead[0]+'</h6></li>'
        lead_users_taglist.push(lead_users_tag);
    }else{
        for (let i=0; i<(lead).length;i++){
            lead_list.push(lead[i])
        }
        let combine_leads = lead_list.join(" | ");
        let lead_users_tag = '<li class="offical_heads"><span>Current Team Leads</span><h6>'+combine_leads+'</h6></li>'
        lead_users_taglist.push(lead_users_tag);
    }
    let added_leads = lead_users_taglist.join("");
    let final_tags = officals_tag + added_leads

    let heads_litags = $('.js_officals li.offical_heads');
    if(heads_litags.length == 0){
        $('ul.js_officals').append(final_tags)
    }else{
        heads_litags.remove()
        $('ul.js_officals').append(final_tags)
    }

    var user_data_list = []
    $.each(data_storage['project_user_data'][project_name], function(id_, element){
        user_data_list = user_data_list.concat(element);
    });

    let added_user_list = [];
    let constrain_list = [];
    let total_users = [];
    var designation_dict = {}

    for (let i=0; i<(user_data_list).length;i++){
        if(project_name == user_data_list[i][2] && user_data_list[i][5] == 'Active'){
            total_users.push(user_data_list[i][0].split('-')[0])
            designation_dict[user_data_list[i][7]] = []
            constrain_list.push(user_data_list[i][0].split('-')[0].trim()+'_'+user_data_list[i][7])
            for (let j=0; j<(constrain_list).length;j++){
                if(constrain_list[j].split('_')[1] == user_data_list[i][7]){
                    designation_dict[user_data_list[i][7]].push(constrain_list[j].split('_')[0])
                }
            }
        }
    }

    let segemnt_tags = []
    $.each(designation_dict, function(desig, desig_users){
        let header_tag = '<h6 class="desig_header">'+desig+' [ '+desig_users.length+' ]</h6>'
        let body_user_list = [];
        for (let i=0; i<(desig_users).length;i++){
            let users_tag = '<li class="col-md-3 user_name">&#9701; '+desig_users[i]+'</li>'
            body_user_list.push(users_tag)
        }
        body_user_list = body_user_list.join("")
        segemnt_tags.push(header_tag+body_user_list)
    });

    let user_litags = $('.js_users li');
    let header_litags = $('.js_users h6.desig_header');
    if(user_litags.length == 0 && header_litags.length == 0){
        $('ul.js_users').append(segemnt_tags)
    }else{
        user_litags.remove()
        header_litags.remove()
        $('ul.js_users').append(segemnt_tags)
    }
    $('.user_count').text(total_users.length);
}


/*################################################### Admin Progress ###############################################################*/
$('.admin_projects').on('click', function(){
    $('#popup_projects').fadeIn(1000);
    let popup_project_list = []
    $.each(data_storage['employee_projects'], function(id_, element){
        if(element['status'] == 'Active'){
            let popup_project_tag = '<li class="col-md-2 popup_project_name"><button type="button" class="popup_profile_project" onclick="ClickedON_Popup_Projects(event)" value="'+id_+'">'+id_+'</button></li>'
            popup_project_list.push(popup_project_tag);
        }
    });
    let added_projects = popup_project_list.join("");
    if($('.js_projects li.popup_project_name').length == 0){
        $('ul.js_projects').append(added_projects);
    }else{
        $('.js_projects li.popup_project_name').remove();
        $('ul.js_projects').append(added_projects);
    }
    $('#popup_projects .project_count').text(popup_project_list.length)
});

function ClickedON_Popup_Projects(event){
    $('span.no_users').parent().removeClass('justify-content-center');
    $("#popup_projects").fadeOut(1000);
    $('#popup_users').fadeIn(1000);
    let project_name = event.target.value;
    user_visibility_control(project_name)
}

/*################################################### Business Head Progress ###############################################################*/
$('.profile_project').on('click', function(){
    $('span.no_users').parent().removeClass('justify-content-center');
    $('#popup_users').attr("style","display: block !important");
    let project_name = $(this).text();
    user_visibility_control(project_name)
});


/*################################################### Business Head Overall Progress ###############################################################*/
$('.profile_all_project').on('click', function(){
    $('#overall_popup_projects').fadeIn(1000);
    let popup_project_list = []
    $.each(data_storage['employee_projects'], function(id_, element){
        if (element['status'] == 'Active'){
            let heads_result = heads_content(id_, element['project_id'])
            let users_result = users_content(id_, element['project_id'])
            let popup_project_tag = '<div id="overall_project_content" data-aos="fade-up"><span class="overall_project_count">'+users_result[1]+'</span><label class="tag_label">Users</label><h4 class="overall_project_header">'+id_+'</h4><ul class="row overall_project_body"><div class="row heads_block">'+heads_result+'</div><div class="row users_block">'+users_result[0]+'</div></ul></div>'
            popup_project_list.push(popup_project_tag);
        }
    });
    let added_projects = popup_project_list.join("");
    if($('.overall_projects #overall_project_content').length == 0){
        $('ul.overall_projects').append(added_projects);
    }else{
        $('.overall_projects #overall_project_content').remove();
        $('ul.overall_projects').append(added_projects);
    }
});


function heads_content(project_name, project_id){
    let heads_dict = {}
    heads_dict['business_head'] = []
    heads_dict['manager'] = []
    heads_dict['lead'] = []
    $.each(data_storage['employee_projects'][project_name]['process'], function(id_, element){
        business_head = unquie_list(heads_dict['business_head'], element['business_head'])
        manager = unquie_list(heads_dict['manager'], element['manager'])
        lead = unquie_list(heads_dict['lead'], element['lead'])
    });

    var user_data_list = []
    $.each(data_storage['project_user_data'][project_name], function(id_, element){
        user_data_list = user_data_list.concat(element);
    });
    let inactive_leads = []
    $.each(heads_dict['lead'], function(ind_, elemen_){
        for (let i=0; i<(user_data_list).length;i++){
            if(user_data_list[i][0].split('-')[0].trim() == elemen_ && user_data_list[i][5] == "Inactive"){
                inactive_leads.push(user_data_list[i][0].split('-')[0].trim())
            }
        }
    });
    for( var i = 0; i < heads_dict['lead'].length; i++){ 
        if ( heads_dict['lead'][i] == inactive_leads[0]) { 
            heads_dict['lead'].splice(i, 1);
        }
    }
    if(heads_dict['lead'].length == 0){
        heads_dict['lead'].push(heads_dict['manager'][0])
    }


    officals_tag = '<li class="offical_heads"><span>Business Head</span><h6>'+business_head[0]+'</h6></li><li class="offical_heads"><span>Project Manager</span><h6>'+manager[0]+'</h6></li>'
    let lead_users_taglist = []
    let lead_list = []
    if(lead.length == 1){
        let lead_users_tag = '<li class="offical_heads"><span>Current Team Lead</span><h6>'+lead[0]+'</h6></li>'
        lead_users_taglist.push(lead_users_tag);
    }else{
        for (let i=0; i<(lead).length;i++){
            lead_list.push(lead[i])
        }
        let combine_leads = lead_list.join(" | ");
        let lead_users_tag = '<li class="offical_heads"><span>Current Team Leads</span><h6>'+combine_leads+'</h6></li>'
        lead_users_taglist.push(lead_users_tag);
    }
    let added_leads = lead_users_taglist.join("");
    let final_tags = officals_tag + added_leads
    return final_tags
}

function users_content(project_name, project_id){
    var user_data_list = []
    $.each(data_storage['project_user_data'][project_name], function(id_, element){
        user_data_list = user_data_list.concat(element);
    });

    let added_user_list = [];
    let constrain_list = [];
    let total_users = [];
    var designation_dict = {}

    for (let i=0; i<(user_data_list).length;i++){
        if(project_name == user_data_list[i][2] && user_data_list[i][5] == 'Active'){
            total_users.push(user_data_list[i][0].split('-')[0])
            designation_dict[user_data_list[i][7]] = []
            constrain_list.push(user_data_list[i][0].split('-')[0].trim()+'_'+user_data_list[i][7])
            for (let j=0; j<(constrain_list).length;j++){
                if(constrain_list[j].split('_')[1] == user_data_list[i][7]){
                    designation_dict[user_data_list[i][7]].push(constrain_list[j].split('_')[0])
                }
            }
        }
    }

    let segemnt_tags = []
    $.each(designation_dict, function(desig, desig_users){
        let header_tag = '<h6 class="desig_header">'+desig+' [ '+desig_users.length+' ]</h6>'
        let body_user_list = [];
        for (let i=0; i<(desig_users).length;i++){
            let users_tag = '<li class="col-md-3 user_name">&#9701; '+desig_users[i]+'</li>'
            body_user_list.push(users_tag)
        }
        body_user_list = body_user_list.join("")
        segemnt_tags.push(header_tag+body_user_list)
    });
    segemnt_tags = segemnt_tags.join("")
    return [segemnt_tags, total_users.length]
}