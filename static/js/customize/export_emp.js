$('.emp_export').on('click', function(){
    var th_value = "";
    var thead_list = [];
    var thead_value = "";
    var tbody_list = [];
    $('#ms_table thead tr th').each(function(){
        th_value = "<th>"+$(this).text()+"</th>"
        thead_list.push(th_value)
    });
    thead_value = "<thead>"+thead_list.join('')+"</thead>";
    $('#ms_table tbody tr').each(function(){
        tbody_list.push("<tr>")
        $('td',this).each(function(){
            tbody_list.push("<td>"+$(this).text()+"</td>")
        });
        tbody_list.push("</tr>")
    });
    tbody_value = "<tbody>"+tbody_list.join('')+"</tbody>"
    table_value = thead_value+tbody_value
    if ($('#dup_table thead').length == 0){
        $('#dup_table').append(table_value)
    }
    else{
        $('#dup_table thead').remove();
        $('#dup_table tbody').remove();
        $('#dup_table').append(table_value)
    }
    setTimeout(3)
    /*let table = document.getElementsByTagName('table');
    TableToExcel.convert(table[0],{
        name: 'Employee Entry Report.xlsx',
        headers: true,     
        sheet:{
            name: 'Employee Entry Report'
        }
    });*/
    let table = document.querySelector('#dup_table');
    TableToExcel.convert(table,{
        name: 'Employee Entry Report.xlsx',
        headers: true,     
        sheet:{
            name: 'Employee Entry Report'
        }
    });
});


$('.notlogin_export').on('click', function(){
    var th_value = "";
    var thead_list = [];
    var thead_value = "";
    var tbody_list = [];
    $('#not_login_table thead tr th').each(function(){
        th_value = "<th>"+$(this).text()+"</th>"
        thead_list.push(th_value)
    });
    thead_value = "<thead>"+thead_list.join('')+"</thead>";
    $('#not_login_table tbody tr').each(function(){
        tbody_list.push("<tr>")
        $('td',this).each(function(){
            tbody_list.push("<td>"+$(this).text()+"</td>")
        });
        tbody_list.push("</tr>")
    });
    if(tbody_list[1].includes('>0<')){
       $('.popup_notlogin_list bold').text("Please select the Single Date")
    }else{
       $('.popup_notlogin_list bold').text("")
        tbody_value = "<tbody>"+tbody_list.join('')+"</tbody>"
        table_value = thead_value+tbody_value
        if ($('#att_dup_login_table thead').length == 0){
            $('#att_dup_login_table').append(table_value)
        }
        else{
            $('#att_dup_login_table thead').remove();
            $('#att_dup_login_table tbody').remove();
            $('#att_dup_login_table').append(table_value)
        }
        setTimeout(3)
        let table = document.querySelector('#att_dup_login_table');
        TableToExcel.convert(table,{
            name: 'Attendance - Not Entry Report.xlsx',
            headers: true,     
            sheet:{
                name: 'Not Login'
            }
        });
    }
});

$('.logout_export').on('click', function(){
    var th_value = "";
    var thead_list = [];
    var thead_value = "";
    var tbody_list = [];
    $('#not_logout_table thead tr th').each(function(){
        th_value = "<th>"+$(this).text()+"</th>"
        thead_list.push(th_value)
    });
    thead_value = "<thead>"+thead_list.join('')+"</thead>";
    $('#not_logout_table tbody tr').each(function(){
        tbody_list.push("<tr>")
        $('td',this).each(function(){
            tbody_list.push("<td>"+$(this).text()+"</td>")
        });
        tbody_list.push("</tr>")
    });
    if(tbody_list[1].includes('>0<')){
       $('.popup_logout_list bold').text("Please select the Single Date")
    }else{
       $('.popup_logout_list bold').text("")
        tbody_value = "<tbody>"+tbody_list.join('')+"</tbody>"
        table_value = thead_value+tbody_value
        if ($('#att_dup_logout_table thead').length == 0){
            $('#att_dup_logout_table').append(table_value)
        }
        else{
            $('#att_dup_logout_table thead').remove();
            $('#att_dup_logout_table tbody').remove();
            $('#att_dup_logout_table').append(table_value)
        }
        setTimeout(5)
        let table = document.querySelector('#att_dup_logout_table');
        TableToExcel.convert(table,{
            name: 'Attendance - Not Log-Off Report.xlsx',
            headers: true,     
            sheet:{
                name: 'Not Logoff'
            }
        });
    }
});