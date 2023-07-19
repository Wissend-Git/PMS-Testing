$(document).ready(function() {

    let window_height = $(window).height();
    let header_height = $(".header_block").height();
    $("#body_content .container-fluid").css("padding-top",header_height);
    $('#body_content .container-fluid').css("height", window_height-header_height-1);
    $(".counter").counterUp({delay:5,time:200});

    $("#header_width").css("width", $("#data_table").width());
});

$(".analysis_module").on('click', function(){
    let div_id = $(this).attr("id");
    window.location = "\master_data?id="+div_id;
});

