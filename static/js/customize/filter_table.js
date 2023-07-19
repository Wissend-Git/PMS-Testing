$(document).ready(function($){
    $('#data_table thead th select').each(function(){
        var found = [];
        var header_id = $(this).attr("id");
        $(this).find("option").each(function(index, val){
            if (found.indexOf(val['value']) == -1){
                found.push(val['value']);
            }else{
                val.remove();
            }
        });

    if(data_storage['report_type'] == 'Quality Assurance'){
        $('button.file_tablink').css({'color':'#fff','background-color': '#00c9cc', 'font-size': '15px'})
        footer_set('file')
    }else{
        $('button.user_tablink').css({'color':'#fff','background-color': '#00c9cc', 'font-size': '15px'})
        footer_set('user')
    }

    revert_form_edit()
    footer_set('general')
    sort_select_option('select[id="'+header_id+'"]', 2)
    $('#data_table thead th #file_Filename').css('width', '140px');
    $('#data_table thead tr th select#Comments').css('width', '90px')
    $('#data_table thead tr th select#file_Cmts').css('width', '60px')
	});
    $('[data-toggle="tooltip"]').tooltip();
    filters_adding()
});

var data_storage = JSON.parse(my_storage);
var data_quality = JSON.parse(quality_summary);

var global_rcvd_index = $('#data_table th select#user_Rcvd').parent().index()
var global_audited_index = $('#data_table th select#user_Audit').parent().index()
var default_users_recieved = parseInt($('td.users_recieved').text())
var default_users_audited = parseInt($('td.users_audited').text())
var default_files_recieved = parseInt($('td.files_recieved').text())
var default_files_audited = parseInt($('td.files_audited').text())

function default_mode(){
    $('td.users_recieved').text(default_users_recieved)
    $('td.users_audited').text(default_users_audited)
    $('td.files_recieved').text(default_files_recieved)
    $('td.files_audited').text(default_files_audited)
    filters_adding()
}

$(window).scroll(function(){
    if($(this).scrollTop()>10){$('.overall_qc_reports').hide(1000);}else{$('.overall_qc_reports').show(1000);}
});


function files_checking_moment(selection_filters, filter_in){
    let matched_rcvd_files = []
    let matched_audit_files = []
    let default_checker = ''
    $.each(selection_filters, function(skey, sval){
        if(['Date', 'Project', 'Process', 'Q-Type'].includes(skey.split('_')[1])){
            if(skey == sval){
                default_checker = 'Default Header'
            }else{
                default_checker = 'Selected Header'
            }
            if('users' == filter_in){
                $(data_quality['overall_users_data']).each(function(FCI, FCD){
                    if(FCD.includes(sval)){
                        matched_rcvd_files.push(parseInt(FCD[global_rcvd_index]))
                        matched_audit_files.push(parseInt(FCD[global_audited_index]))
                    }
                });
            }else{
                $(data_quality['overall_files_data']).each(function(UCI, UCD){
                    if(UCD.includes(sval)){
                        matched_rcvd_files.push(parseInt(UCD[global_rcvd_index]))
                        matched_audit_files.push(parseInt(UCD[global_audited_index]))
                    }
                });
            }
        }

        if(['Quser', 'Puser', 'Filename'].includes(skey.split('_')[1])){
            if(skey == sval){
                default_checker = 'Default Header'
            }else{
                default_checker = 'Selected Header'
            }
            if('users' == filter_in){
                $(data_quality['overall_users_data']).each(function(FCI, FCD){
                    if(FCD[selection_filters['col_index']] == sval){
                        matched_rcvd_files.push(parseInt(FCD[global_rcvd_index]))
                        matched_audit_files.push(parseInt(FCD[global_audited_index]))
                    }
                });
            }else{
                $(data_quality['overall_files_data']).each(function(UCI, UCD){
                    if(UCD[selection_filters['col_index']] == sval){
                        matched_rcvd_files.push(parseInt(UCD[global_rcvd_index]))
                        matched_audit_files.push(parseInt(UCD[global_audited_index]))
                    }
                });
            }
        }
    });
    return [matched_rcvd_files, matched_audit_files, default_checker]
}

/* ################################################################ Filter tabele ################################################################ */
function filter_table(select_tag){
    var col_type = $(select_tag).attr("id");
    let table_headers = $('#data_table thead tr').find('th');
    $(table_headers).each(function(index, col_data){
        let value = $(col_data).find('select option[value="'+col_type+'"]');
        if (value.length == 1){
            let dataset = $('#data_table tbody').find('tr');
            dataset.show();
            let selection = $('select[id="'+col_type+'"]').val();
            dataset.filter(function(data_index, item){
                if (selection == col_type){
                    return false;
                }else{
                    return_filter_data = $(item).find('td:nth-child('+(index+1)+')').text() != selection;
                    return return_filter_data;
                }
            }).hide();
        }
    });
    footer_set('general')
    sort_select_option('select[id="'+col_type+'"]', 2)
}

function user_filter_table(select_tag){
    let selection_filters = {}
    var col_type = $(select_tag).attr("id");
    let table_headers = $('#data_table thead tr').find('th.user_hearder');
    $(table_headers).each(function(index, col_data){
        let value = $(col_data).find('select option[value="'+col_type+'"]');
        if (value.length == 1){
            let dataset = $('#data_table tbody').find('tr.user_report_row');
            dataset.show();
            let selection = $('select[id="'+col_type+'"]').val();
            selection_filters[col_type] = selection
            selection_filters['col_index'] = index
            dataset.filter(function(data_index, item){
                if (selection == col_type){
                    return false;
                }else{
                    return_filter_data = $(item).find('td:nth-child('+(index+1)+')[value^="user_"]').text() != selection;
                    return return_filter_data;
                }
            }).hide();
        }
    });
    footer_set('user')
    sort_select_option('select[id="'+col_type+'"]', 2)
    let collected_moments = files_checking_moment(selection_filters, 'files')
    moments_adding(collected_moments, 'FromUsers')
}

function file_filter_table(select_tag){
    let selection_filters = {}
    var col_type = $(select_tag).attr("id");
    let table_headers = $('#data_table thead tr').find('th.file_hearder');
    $(table_headers).each(function(index, col_data){
        let value = $(col_data).find('select option[value="'+col_type+'"]');
        if (value.length == 1){
            let dataset = $('#data_table tbody').find('tr.file_report_row');
            dataset.show();
            let selection = $('select[id="'+col_type+'"]').val();
            selection_filters[col_type] = selection
            selection_filters['col_index'] = index
            dataset.filter(function(data_index, item){
                if (selection == col_type){
                    return false;
                }else{
                    if(col_type == "file_Filename"){
                        return_filter_data = $(item).find('td:nth-child('+(index+1)+')[value^="file_"] p').text() != selection;
                    }else{
                        return_filter_data = $(item).find('td:nth-child('+(index+1)+')[value^="file_"]').text() != selection;
                    }
                    return return_filter_data;
                }
            }).hide();
        }
    });
    footer_set('file')
    sort_select_option('select[id="'+col_type+'"]', 2)
    let collected_moments = files_checking_moment(selection_filters, 'users')
    moments_adding(collected_moments, 'FromFiles')
}
/* ################################################################ Filter tabele ################################################################ */

function sort_select_option(css_selector, start_index){
    let css_selector_list = css_selector.split(" option");
    let css_selector_name = css_selector_list[0];
    $(css_selector_name).append($(css_selector_name+" option:nth-child(1n+"+start_index+")").remove().sort(function(a, b){ 
        var at = $(a).text(), 
            bt = $(b).text();
        if (isNaN(at) == false && isNaN(bt) == false){
            at = parseInt(at);
            bt = parseInt(bt);
        }
        return (at > bt) ? 1 : ((at < bt) ? -1 : 0);
    }));
}

// ################ Modified Options #########################
/* ################################################################ Filter Set Display ################################################################ */

function filter_set(select_tag){
    let filter_index_number = $(select_tag).attr('value');
    let checked = $(select_tag).is(':checked');
    let index_num = filter_index_number;
    if (checked == false){
        $('#data_table thead tr th:nth-child('+index_num+')').css("display","none");
        $("#data_table tbody tr td:nth-child("+index_num+")").css("display","none");
        $("tfoot tr td:nth-child("+index_num+")").css("display","none");    
    }else{
        $('#data_table thead tr th:nth-child('+index_num+')').css("display","table-cell");
        $("#data_table tbody tr td:nth-child("+index_num+")").css("display","table-cell");
        $("tfoot tr td:nth-child("+index_num+")").css("display","table-cell"); 
    }
}

function user_filter_set(select_tag){
    let filter_index_number = $(select_tag).attr('value');
    let checked = $(select_tag).is(':checked');
    let index_num = filter_index_number.split('_')[1].toString();
    if (checked == false){
        $('#user_report #data_table thead tr th:nth-child('+index_num+')').css("display","none");
        $("#user_report #data_table tbody tr td:nth-child("+index_num+")").css("display","none");
        $("#user_report #data_table tfoot tr td:nth-child("+index_num+")").css("display","none");    
    }else{
        $('#user_report #data_table thead tr th:nth-child('+index_num+')').css("display","table-cell");
        $("#user_report #data_table tbody tr td:nth-child("+index_num+")").css("display","table-cell");
        $("#user_report #data_table tfoot tr td:nth-child("+index_num+")").css("display","table-cell"); 
    }
}

function file_filter_set(select_tag){
    let filter_index_number = $(select_tag).attr('value');
    let checked = $(select_tag).is(':checked');
    let index_num = filter_index_number.split('_')[1].toString();
    if (checked == false){
        $('#file_report #data_table thead tr th:nth-child('+index_num+')').css("display","none");
        $("#file_report #data_table tbody tr td:nth-child("+index_num+")").css("display","none");
        $("#file_report #data_table tfoot tr td:nth-child("+index_num+")").css("display","none");    
    }else{
        $('#file_report #data_table thead tr th:nth-child('+index_num+')').css("display","table-cell");
        $("#file_report #data_table tbody tr td:nth-child("+index_num+")").css("display","table-cell");
        $("#file_report #data_table tfoot tr td:nth-child("+index_num+")").css("display","table-cell"); 
    }
}
/* ################################################################ Filter Set Display ################################################################ */

function footer_set(instruct){
    let user_report_display = $('.report_content #user_report').attr('style');
    let file_report_display = $('.report_content #file_report').attr('style');
    let magnet_filter_headers = ''

    if(user_report_display != undefined && user_report_display.includes("block") == true){
        magnet_filter_headers = $('#data_table thead tr th.user_hearder');
    }else if(file_report_display != undefined && file_report_display.includes("block") == true){
        magnet_filter_headers = $('#data_table thead tr th.file_hearder');
    }else{
        magnet_filter_headers = $('#data_table thead tr th');
    }

    magnet_table_dict = {};
    header_index_list = []
    footer_total_collector = {}

    $.each(magnet_filter_headers, function(index, col_data){
        let magnet_index = index;
        let magnet_name = $(col_data).find('select').attr('id');
        magnet_table_dict[magnet_name] = []
        if(magnet_name.includes("user_") == true){
            let table_rows = $('#data_table tbody').find('tr.user_report_row');
            $.each(table_rows, function(index, col_data){
                let check_style = ($(col_data).attr('style'));
                if (check_style == undefined || check_style.includes('none') == false){
                    let table_row_values = $(col_data).find('td[value^="user_"]');
                    magnet_table_dict[magnet_name].push(table_row_values[magnet_index].innerText)
                }
            });
        }else if(magnet_name.includes("file_") == true){
            let table_rows = $('#data_table tbody').find('tr.file_report_row');
            $.each(table_rows, function(index, col_data){
                let check_style = ($(col_data).attr('style'));
                if (check_style == undefined || check_style.includes('none') == false){
                    let table_row_values = $(col_data).find('td[value^="file_"]');
                    magnet_table_dict[magnet_name].push(table_row_values[magnet_index].innerText)
                }
            });
        }else{
            let table_rows = $('#data_table tbody').find('tr');
            $.each(table_rows, function(index, col_data){
                let check_style = ($(col_data).attr('style'));
                if (check_style == undefined || check_style.includes('none') == false){
                    let table_row_values = $(col_data).find('td');
                    magnet_table_dict[magnet_name].push(table_row_values[magnet_index].innerText)
                }
            });
        }
    });

    var index_num = 1;
    $.each(magnet_table_dict, function(item, item_val){
        var string_list_uniques = [];
        var integer_number = 0;
        var hour_data = 0;
        var mins_data = 0;
        var total_achieved = 0;
        var total_target = 0;
        var cmts_list_uniques = []
        var rvrt_list_uniques = []

        if(item.includes('Prod') == true){
            let total_achieved = $('tfoot tr td[value*="Achieved"]')[0].innerText;
            let total_target = $('tfoot tr td[value*="Target"]')[0].innerText;
            let productivity_average = Math.round((parseInt(total_achieved)/parseInt(total_target))*100);
            $("tfoot tr td:nth-child("+(parseInt(index_num))+")").text(productivity_average);
            index_num+=1;
        }else if(item.includes('Qlty') == true){
            if (instruct == 'file'){
                let file_total_errors = $('tfoot tr td[value*="file_Total"]')[0].innerText;
                let file_total_audited = $('tfoot tr td[value*="file_Audit"]')[0].innerText;
                let file_quality_percentage = ((1 - (parseInt(file_total_errors)/parseInt(file_total_audited)))*100).toFixed(2);
                $("tfoot tr td:nth-child("+(parseInt(index_num))+")").text(file_quality_percentage);
            }else{
                if(data_storage['report_type'] == "Quality Assurance"){}else{
                    let user_total_errors = $('tfoot tr td[value*="user_Total"]')[0].innerText;
                    let user_total_audited = $('tfoot tr td[value*="user_Audit"]')[0].innerText;
                    let user_quality_percentage = ((1 - (parseInt(user_total_errors)/parseInt(user_total_audited)))*100).toFixed(2);
                    $("tfoot tr td:nth-child("+(parseInt(index_num))+")").text(user_quality_percentage);
                }
            }
            index_num+=1;
        }else if(item.includes('Smpl') == true){
            if (instruct == 'file'){
                let file_total_audit = $('tfoot tr td[value*="file_Audit"]')[0].innerText;
                let file_total_recieved = $('tfoot tr td[value*="file_Rcvd"]')[0].innerText;
                let file_sampling_percentage = ((parseInt(file_total_audit)/parseInt(file_total_recieved))*100).toFixed(2);
                $("tfoot tr td:nth-child("+(parseInt(index_num))+")").text(file_sampling_percentage);
            }else{
                if(data_storage['report_type'] == "Quality Assurance"){}else{
                    let user_total_audit = $('tfoot tr td[value*="user_Audit"]')[0].innerText;
                    let user_total_recieved = $('tfoot tr td[value*="user_Rcvd"]')[0].innerText;
                    let user_sampling_percentage = ((parseInt(user_total_audit)/parseInt(user_total_recieved))*100).toFixed(2);
                    $("tfoot tr td:nth-child("+(parseInt(index_num))+")").text(user_sampling_percentage);
                }
            }
            index_num+=1;
        }else{
            if(item.includes("user_") == true){
                moderate_item = item.split('user_')[1]
                query_id = '[value^="user_"]'
            }else if(item.includes("file_") == true){
                moderate_item = item.split('file_')[1]
                query_id = '[value^="file_"]'
            }else{
                moderate_item = item
                query_id = ''
            }


            $.each(item_val, function(i, magnet_el){
                if('Revert' == moderate_item){
                    let row_table = $('#data_table tbody tr #revert_row')
                    rvrt_list_uniques.push(row_table.length)
                }
                if(isNaN(magnet_el)){
                    if('Hours' == moderate_item){
                        let hours= parseFloat(magnet_el.split(' ')[0].replace('h'));
                        let mins= parseFloat(magnet_el.split(' ')[1].replace('m'));
                        mins_data += mins;
                        let q_min = Math.floor(mins_data/60);
                        let r_min = (mins_data%60);
                        temp_hours = q_min+hours
                        hour_data += temp_hours;
                        let total_time = (parseFloat(hour_data+"."+r_min));
                        integer_number = total_time;
                        if(mins_data == 60){
                            mins_data = 0
                        }
                    }else if('Cmts' == moderate_item || 'Comments' == moderate_item){
                        cmts_list_uniques.push(magnet_el)
                    }else{
                        if(string_list_uniques.includes(magnet_el) == false){
                            if($.inArray(magnet_el, string_list_uniques) === -1) string_list_uniques.push(magnet_el)
                            integer_number ++;
                        }
                    }
                }else{
                    if('Year' == moderate_item || 'Week' == moderate_item){
                        if(string_list_uniques.includes(magnet_el) == false){
                            if($.inArray(magnet_el, string_list_uniques) === -1) string_list_uniques.push(magnet_el)
                            integer_number ++;
                        }
                    }else{
                        integer_number += parseInt(magnet_el)
                    }
                }
            });
            if('Cmts' == moderate_item || 'Comments' == moderate_item){
                $('tfoot tr td:nth-child('+(parseInt(index_num))+')'+query_id).text(cmts_list_uniques.length);
                index_num+=1;
            }else if('Revert' == moderate_item){
                $('tfoot tr td:nth-child('+(parseInt(index_num))+')'+query_id).text(rvrt_list_uniques.length);
                index_num+=1;
            }else{
                $('tfoot tr td:nth-child('+(parseInt(index_num))+')'+query_id).text(integer_number);
                index_num+=1;
            }
        }
    });
}


/* ################################################################ Click Filter button ################################################################ */
$(".filter_dropdown").on('click',function(){
    let css_display = $(".filter_dropdown_content").attr('style');
    if (css_display == undefined || css_display.includes("block") == false){
        $(".filter_dropdown_content").css('display','block');
    }else{
        $(".filter_dropdown_content").css('display','none');
    }
});

$(".user_filter_dropdown").on('click',function(){
    let css_display = $(".user_filter_dropdown_content").attr('style');
    if (css_display == undefined || css_display.includes("block") == false){
        $(".user_filter_dropdown_content").css('display','block');
    }else{
        $(".user_filter_dropdown_content").css('display','none');
    }
});

$(".file_filter_dropdown").on('click',function(){
    let css_display = $(".file_filter_dropdown_content").attr('style');
    if (css_display == undefined || css_display.includes("block") == false){
        $(".file_filter_dropdown_content").css('display','block');
    }else{
        $(".file_filter_dropdown_content").css('display','none');
    }
});
/* ################################################################ Click Filter button ################################################################ */

/* ################################################################ Tab Movement ################################################################ */
function moveReport(evt, tabname){
    var iter, tabcontent, tablinks;
    if(tabname == 'user_report'){
        $('#user_report').css('display','block');
        $('#file_report').css('display','none');
        $('button.user_tablink').css({'color':'#fff','background-color': '#00c9cc', 'font-size': '15px'})
        $('button.file_tablink').css({'color':'#000','background-color': 'transparent', 'font-size': '13px'})
        footer_set('user')
    }else{
        $('#user_report').css('display','none');
        $('#file_report').css('display','block');
        $('button.file_tablink').css({'color':'#fff','background-color': '#00c9cc', 'font-size': '15px'})
        $('button.user_tablink').css({'color':'#000','background-color': 'transparent', 'font-size': '13px'})
        footer_set('file')
    }
    filters_adding()
}
/* ################################################################ Tab Movement ################################################################ */
// ################ Modified Options #########################
function revert_form_edit(){
    var edit_row = $('#data_table tbody #revert_row');
    var revert_headers = $('#data_table thead tr th.file_hearder');

    for (var i = 0; i < edit_row.length; i++){
        edit_row[i].addEventListener('click', function(e){
            document.getElementById('revertion').style.display = 'block';
            var tr_parent = this.parentNode;
            $.each(revert_headers, function(i, ele){
                let column_header_id = $(ele).find('select').attr('id').split('_')[1];
                document.getElementById(column_header_id).value = tr_parent.querySelector('.row_'+column_header_id).innerText;
            });
        }, false);
    }
}

// ################ Working on Summary Filteration #########################
function filters_adding(){
    let filters_users_recieved = parseInt($('td.users_recieved').text())
    let filters_users_audited = parseInt($('td.users_audited').text())
    let filters_files_recieved = parseInt($('td.files_recieved').text())
    let filters_files_audited = parseInt($('td.files_audited').text())
    // if(data_quality['overall_files_data'].length != 0){
    //     filters_files_recieved = parseInt($('td.files_recieved').text())
    //     filters_files_audited = parseInt($('td.files_audited').text())
    // }
    let total_recieved = filters_users_recieved + filters_files_recieved
    let total_audited = filters_users_audited + filters_files_audited

    $('td.total_recieved p').text(total_recieved)
    $('td.total_audited p').text(total_audited)
}

function moments_adding(collected_moments, moment_cache){
    if(moment_cache == 'FromUsers'){
        let for_adding_users_recieved = $('tfoot td[value="user_Rcvd"]').text()
        let for_adding_users_audited = $('tfoot td[value="user_Audit"]').text()

        if(collected_moments.length != 0){
            if(collected_moments[2] == 'Default Header'){
                default_mode()
            }else{
                $('td.users_recieved').text(for_adding_users_recieved)
                $('td.users_audited').text(for_adding_users_audited)
                $('td.files_recieved').text(collected_moments[0].reduce((a,b) => a+b, 0))
                $('td.files_audited').text(collected_moments[1].reduce((a,b) => a+b, 0))
            }
        }else{
            if(collected_moments[2] == 'Default Header'){
                default_mode()
            }else{
                $('td.users_recieved').text(for_adding_users_recieved)
                $('td.users_audited').text(for_adding_users_audited)
                $('td.files_recieved').text(0)
                $('td.files_audited').text(0)
            }
        }
    }else if(moment_cache == 'FromFiles'){
        let for_adding_files_recieved = $('tfoot td[value="file_Rcvd"]').text()
        let for_adding_files_audited = $('tfoot td[value="file_Audit"]').text()
        if(collected_moments.length != 0){
            if(collected_moments[2] == 'Default Header'){
                default_mode()
            }else{
                $('td.files_recieved').text(for_adding_files_recieved)
                $('td.files_audited').text(for_adding_files_audited)
                $('td.users_recieved').text(collected_moments[0].reduce((a,b) => a+b, 0))
                $('td.users_audited').text(collected_moments[1].reduce((a,b) => a+b, 0))
            }
        }else{
            if(collected_moments[2] == 'Default Header'){
                default_mode()
            }else{
                $('td.users_recieved').text(0)
                $('td.users_audited').text(0)
                $('td.files_recieved').text(for_adding_files_recieved)
                $('td.files_audited').text(for_adding_files_audited)
            }
        }
    }
    filters_adding()
}

/* ############################################################# Export Content ############################################################# */
/*function export_old_data(){
    var tabularData = [{"sheetName": "Data"}];
    let user_report_display = $('.report_content #user_report').attr('style');
    let file_report_display = $('.report_content #file_report').attr('style');

    let tab_ex = 0
    let magnet_filter_headers = ''
    if(user_report_display != undefined && user_report_display.includes("block") == true){
        magnet_filter_headers = $('#data_table thead tr th.user_hearder[style="top: 60px;"]');
        tab_ex = 1
    }else if(file_report_display != undefined && file_report_display.includes("block") == true){
        magnet_filter_headers = $('#data_table thead tr th.file_hearder[style="top: 60px;"]');
        tab_ex = 2
    }else{
        magnet_filter_headers = $('#data_table thead tr th[style="top: 60px;"]');
        tab_ex = 0
    }

    let export_body = []
    let deen_header = []
    $.each(magnet_filter_headers, function(index, col_data){
        let magnet_name = $(col_data).find('select').attr('id');
        if(tab_ex == 1){final_header = magnet_name.replace('user_','')}
        else if(tab_ex == 2){final_header = magnet_name.replace('file_','')}
        else{final_header = magnet_name}
        deen_header.push({'text': final_header})
    });
    export_body.push(deen_header)

    if(tab_ex == 1){
        let export_tr = $('#data_table tbody').find('tr.user_report_row');
        let determine = []
        $.each(export_tr, function(index, col_data){
            let export_table_body = []
            $(col_data).find('td[value^="user_"]').each(function(en, elsss){
                if($(elsss).attr('style') == undefined || $(elsss).attr('style').includes('none') == false){
                    if($(elsss).find('p').length == 1){
                        let tab_data = $(elsss).find("p").attr('data-original-title').toString()
                        export_table_body.push({'text': tab_data})
                    }else{
                        let tab_data = $(elsss).text().toString()
                        export_table_body.push({'text': tab_data})
                    }
                }
            });
            export_body.push(export_table_body)
        });
    }else if(tab_ex == 2){
        let export_tr = $('#data_table tbody').find('tr.file_report_row');
        let determine = []
        $.each(export_tr, function(index, col_data){
            let export_table_body = []
            $(col_data).find('td[value^="file_"]').each(function(en, elsss){
                if($(elsss).attr('style') == undefined || $(elsss).attr('style').includes('none') == false){
                    if($(elsss).find('p').length == 1){
                        let tab_data = $(elsss).find("p").attr('data-original-title').toString()
                        export_table_body.push({'text': tab_data})
                    }else{
                        let tab_data = $(elsss).text().toString()
                        export_table_body.push({'text': tab_data})
                    }
                }
            });
            export_body.push(export_table_body)
        });
    }else{
        let export_tr = $('#data_table tbody').find('tr');
        let determine = []
        $.each(export_tr, function(index, col_data){
            let export_table_body = []
            $(col_data).find('td').each(function(en, elsss){
                if($(elsss).attr('style') == undefined || $(elsss).attr('style').includes('none') == false){
                    if($(elsss).find('b').length == 1){
                        let tab_data = $(elsss).find("b").attr('data-original-title').toString().trim()
                        export_table_body.push({'text': tab_data})
                    }else{
                        let tab_data = $(elsss).text().toString()
                        export_table_body.push({'text': tab_data})
                    }
                }
            });
            export_body.push(export_table_body)
        });
    }
    tabularData[0]['data'] = export_body
    console.log(tabularData)
    return [tabularData, tab_ex]
}*/

function export_report_type(){
    var report_name = ''
    let productivity_selected = $('#project_filter #select_report_type #productivity_report').is(':checked')
    let teamq_selected = $('#project_filter #select_report_type #team_quality').is(':checked')
    let userq_selected = $('#project_filter #select_report_type #user_quality').is(':checked')
    let assureq_selected = $('#project_filter #select_report_type #assure_quality').is(':checked')
    if(productivity_selected == true && teamq_selected == false && userq_selected == false && assureq_selected == false){
        report_name = 'Productivity'
    }else if(productivity_selected == false && teamq_selected == true && userq_selected == false && assureq_selected == false){
        report_name = 'Team Quality'
    }else if(productivity_selected == false && teamq_selected == false && userq_selected == true && assureq_selected == false){
        report_name = 'Quality User'
    }else if(productivity_selected == false && teamq_selected == false && userq_selected == false && assureq_selected == true){
        report_name = 'Quality Assurance'
    }
    return report_name
}

function export_data(){

    let set_pms_tag = 0
    if(export_report_type() == 'Productivity'){set_pms_tag = 0}
    else if(export_report_type() == 'Team Quality'){set_pms_tag = 1}
    else if(export_report_type() == 'Quality User'){set_pms_tag = 1}
    else if(export_report_type() == 'Quality Assurance'){set_pms_tag = 2}

    let magnet_user_headers = $('#data_table thead tr th.user_hearder[style="top: 60px;"]');
    let magnet_file_headers = $('#data_table thead tr th.file_hearder[style="top: 60px;"]');
    let magnet_prod_headers = $('#data_table thead tr th[style="top: 60px;"]');

    var export_headers = {'prod_header': [], 'user_header': [], 'file_header': []}
    var export_bodies = {'prod_body': [], 'user_body': [], 'file_body': []}

    function body_soda(export_tr, export_body, body_control){
        $.each(export_tr, function(index, col_data){
            let export_table_body = []
            if($(col_data).attr('style') == undefined || $(col_data).attr('style').includes('none') == false){
                $(col_data).find('td[value^="'+body_control+'"]').each(function(en, elsss){
                    if($(elsss).attr('style') == undefined || $(elsss).attr('style').includes('none') == false){
                        if($(elsss).find('p').length == 1){
                            let tab_data = $(elsss).find("p").attr('data-original-title').toString()
                            export_table_body.push({'text': tab_data})
                        }else{
                            let tab_data = $(elsss).text().toString()
                            export_table_body.push({'text': tab_data})
                        }
                    }
                });
                export_body.push(export_table_body)
            }
        });
    }

    if(set_pms_tag == 1){
        let export_user_body = []
        let export_file_body = []
        $(magnet_user_headers).each(function(index, col_data){
            let magnet_name = $(col_data).find('select').attr('id');
            export_headers['user_header'].push({'text': magnet_name.replace('user_','')})
        });
        $(magnet_file_headers).each(function(index, col_data){
            let magnet_name = $(col_data).find('select').attr('id');
            export_headers['file_header'].push({'text': magnet_name.replace('file_','')})
        });
        let export_user_tr = $('#data_table tbody').find('tr.user_report_row');
        let export_file_tr = $('#data_table tbody').find('tr.file_report_row');
        body_soda(export_user_tr, export_bodies['user_body'], 'user_')
        body_soda(export_file_tr, export_bodies['file_body'], 'file_')
    }else if(set_pms_tag == 2){
        $(magnet_file_headers).each(function(index, col_data){
            let magnet_name = $(col_data).find('select').attr('id');
            export_headers['file_header'].push({'text': magnet_name.replace('file_','')})
        });
        let export_file_tr = $('#data_table tbody').find('tr.file_report_row');
        body_soda(export_file_tr, export_bodies['file_body'], 'file_')
    }else if(set_pms_tag == 0){
        $(magnet_prod_headers).each(function(index, col_data){
            let magnet_name = $(col_data).find('select').attr('id');
            export_headers['prod_header'].push({'text': magnet_name})
        });
        let export_prod_tr = $('#data_table tbody').find('tr');
        $.each(export_prod_tr, function(index, col_data){
            let export_table_body = []
            $(col_data).find('td').each(function(en, elsss){
                if($(elsss).attr('style') == undefined || $(elsss).attr('style').includes('none') == false){
                    if($(elsss).find('b').length == 1){
                        let tab_data = $(elsss).find("b").attr('data-original-title').toString().trim()
                        export_table_body.push({'text': tab_data})
                    }else{
                        let tab_data = $(elsss).text().toString()
                        export_table_body.push({'text': tab_data})
                    }
                }
            });
            export_bodies['prod_body'].push(export_table_body)
        });
    }

    var tabularData = ''
    if(export_headers['prod_header'].length != 0){
        let p1 = []
        p1.push(export_headers['prod_header'])
        $(export_bodies['prod_body']).each(function(pp, pcol){p1.push(pcol)});
        tabularData = [{'sheetName': 'Productivity Report', 'data': p1}];
    }else if(export_headers['user_header'].length != 0 && export_headers['file_header'].length != 0){
        let q1 = []
        let q2 = []
        q1.push(export_headers['user_header'])
        q2.push(export_headers['file_header'])
        $(export_bodies['user_body']).each(function(dd, ecol){q1.push(ecol)});
        $(export_bodies['file_body']).each(function(gg, hcol){q2.push(hcol)});
        tabularData = [{'sheetName': 'User Report', 'data': q1}, {'sheetName': 'File Report', 'data': q2}];
    }else if(export_headers['user_header'].length != 0){
        let q1 = []
        q1.push(export_headers['user_header'])
        $(export_bodies['user_body']).each(function(gg, hcol){q1.push(hcol)});
        tabularData = [{'sheetName': 'User Report', 'data': q1}];
    }else if(export_headers['file_header'].length != 0){
        let q2 = []
        q2.push(export_headers['file_header'])
        $(export_bodies['file_body']).each(function(gg, hcol){q2.push(hcol)});
        tabularData = [{'sheetName': 'File Report', 'data': q2}];
    }
    return tabularData
}

function filename_customization(){
    var selected_type = ''

    if($('#check_year').is(':checked') == true){selected_type = 'Yearly'}
    else if($('#check_month').is(':checked') == true){selected_type = 'Monthly'}
    else if($('#check_week').is(':checked') == true){selected_type = 'Weekly'}
    else if($('#check_day').is(':checked') == true){selected_type = 'Daily'}

    var report_name = export_report_type()

    var file_date_range = ''

    let from_date_getter = $('#datepicker input#from_date').attr('value')
    let to_date_getter = $('#datepicker input#to_date').attr('value')
    let selected_year = $('#selected_year select option[selected]').attr('value')
    let selected_month = $('#selected_month select option[selected]').attr('value')
    var month_names = ["Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sep", "Oct", "Nov", "Dec"];
    if(from_date_getter != undefined && to_date_getter != undefined){
        let custom_from_dater = from_date_getter.split('-')[1]+'-'+from_date_getter.split('-')[0]+"-"+from_date_getter.split('-')[2]
        let custom_to_dater = to_date_getter.split('-')[1]+'-'+to_date_getter.split('-')[0]+"-"+to_date_getter.split('-')[2]
        var from_dater = new Date(custom_from_dater);
        var to_dater = new Date(custom_from_dater);
        let custom_from_date = from_date_getter.split('-')[0]+"-"+month_names[from_dater.getMonth()]+"-"+from_date_getter.split('-')[2]
        let custom_to_date = to_date_getter.split('-')[0]+"-"+month_names[to_dater.getMonth()]+"-"+to_date_getter.split('-')[2]
        if(custom_from_date == custom_to_date){
            file_date_range = custom_from_date
        }else{
            file_date_range = custom_from_date+" to "+custom_to_date
        }
    }else{
        if(selected_year != "All" && selected_month == "All"){
            file_date_range = selected_year+" Report"
        }else if(selected_year == "All" && selected_month != "All"){
            file_date_range = month_names[selected_month-1]+"-All Year Report"
        }else if(selected_year == "All" && selected_month == "All"){
            file_date_range = "Complete Report"
        }else{
            file_date_range = month_names[selected_month-1]+"-"+selected_year
        }
    }

    let final_filename = selected_type+' '+report_name+'_'+file_date_range
    return final_filename
}

function export_excel(){
    tabularData = export_data()
    let customize_filename = filename_customization()

    var options = {
        fileName: customize_filename,
        extension: ".xlsx",
        header: true,
        maxCellWidth: 15,
        maxCellHeight: 10,
        maxSize: 10
    };

    if(tabularData.length != 0){
        Jhxlsx.export(tabularData, options);
    }else{
        alert("No Data to Export");
    }

    // var url = 'data.json';
    // $.get(url, {}, function(data){
    //     Jhxlsx.export(data.tabularData_2, data.options);
    // });
    // $.get(url, {}, function (data) {
    //     Jhxlsx.export(data.tabularData, data.options);
    // }).fail(function (jqXHR) {
    //     alert("error: " + jqXHR.status + " / " + jqXHR.statusText);
    // });

}