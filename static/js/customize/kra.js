$(document).ready(function() {

    var user_list = []
    $("#kra_dropdown #myFilter option").each(function(){
        let user_id = $(this).attr("value");
        if (user_list.includes(user_id) == false){
            user_list.push(user_id);
        }else{
            $(this).remove();
        }
    });

    kra_rating_update();
    $("#data_table thead th").each(function(){
        let th_data = $(this).find('select').attr('id');
        let index_num = $(this).index();
        if (th_data == "Achieved" || th_data == "Comments"){
            $("#data_table tbody tr").each(function(){
                let x = $(this).find("td");
                $(this).find(x[index_num]).css('color','#2b7bec')
            });
        }
    });
 
    $(function () {
        $('[data-toggle="tooltip"]').tooltip()
      })

    let kra_status = $("#kra_input").is(":checked");
    if(kra_status == true){
        $('#kra_dropdown #kra_month_range select[name="kra_month_selected"] option').each(function(){
            if(this.value == data_storage['kra_month_selected']){
                $(this).prop("selected",true);
            }else{
                $(this).prop("selected",false);
            }
        });
    }
});


$(".kra_header input[type='radio']").on('click', function(){
    $("#kra_input_error").text("");
    let emp_type = $(this).attr("empt");
    if (["TL",'TLR'].includes(emp_type)){
        $(this).parent().parent().parent().parent().children("div").find(".kra_rating").find("#tl_kra_rating").text($(this).val());
    }else if(["TM","TMR"].includes(emp_type) ){
        $(this).parent().parent().parent().parent().children("div").find(".kra_rating").find("#m_kra_rating").text($(this).val());
    }else{
        $(this).parent().parent().parent().parent().children("div").find(".kra_rating").find("#bh_kra_rating").text($(this).val());
    }
    kra_rating_update();
});

$(".kra_content form button").on('click',function(event){
    $("#kra_input_error").text("");
    $(".kra_content form ul li#kra_content").each(function(){
        let true_num = 0;
        $(this).find("input").each(function(){
            let radio_check = $(this).is(":checked");
            if(radio_check == true){
                true_num = 1;
            }
        });
        if (true_num == 0){
            $("#kra_input_error").text($(this).find("h5").text()+" - input field is not selected");
            event.preventDefault();
            return false;
        }
    });
});

function kra_rating_update(){
    var tl_score = 0;
    var tm_score = 0;
    var bh_score = 0;
    $("ul.kra_header li#kra_content").each(function(){
        let tl_rating = $(this).find(".kra_rating").find("#tl_kra_rating").text();
        let tm_rating = $(this).find(".kra_rating").find("#m_kra_rating").text();
        let bh_rating = $(this).find(".kra_rating").find("#bh_kra_rating").text();
        if (tl_rating.length != 0){
            tl_score = (tl_score + parseInt(tl_rating));
        }
        if (tm_rating.length != 0){
            tm_score = (tm_score + parseInt(tm_rating));
        }
        if (bh_rating.length != 0){
            bh_score = (bh_score + parseInt(bh_rating));
        }
    });
    $("#lead_rating").text(tl_score);
    $("#manager_rating").text(tm_score);
    $("#bh_rating").text(bh_score);
    let emp_type = $("#ach_rating").attr("empt");
    if (['TL', 'TLR'].includes(emp_type)){
        $("#ach_rating").val(tl_score);
    }else if (['TM', 'TMR'].includes(emp_type)){
        $("#ach_rating").val(tm_score);
    }else{
        $("#ach_rating").val(bh_score);
    }
}