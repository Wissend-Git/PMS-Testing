$(document).ready(function($){

    $("#popup_image").css('display', 'none')
    $(".close").on("click", function(e){
        e.preventDefault();
        $("#popup_image").fadeOut(1000);
    });

    document.onkeydown = function(e){
        if(e.keyCode == 27){
            $("#popup_image").fadeOut(1000);
        }
        if(e.keyCode == 37){
            plusSlides(37)
        }
        if(e.keyCode == 39){
            plusSlides(39)
        }
    }

    let images_recieved = [];
    $.each(data_storage['template_image_path'], function(key_, value_){
        if(value_.length != 0){
           images_recieved.push(key_)
        }
    })
    if(images_recieved[0] == 'Announcement'){
        $('button.annouce_tablink').css({'color':'#fff','background-color': '#00b1b3', 'font-size': '15px'})
        $('#gallery_announcement, .global_announcement').css('display','block');
        $('#gallery_anniversary, .global_anniversary').css('display','none');
        $('#gallery_birthday, .global_birthday').css('display','none');
        $('#gallery_celebrate, .global_celebrate').css('display','none');
        $('#gallery_honour, .global_honour').css('display','none');
        $('#no_image').css('display','none');
    }else if(images_recieved[0] == 'Anniversary'){
        $('button.anniversary_tablink').css({'color':'#fff','background-color': '#00b1b3', 'font-size': '15px'})
        $('#gallery_announcement, .global_announcement').css('display','none');
        $('#gallery_anniversary, .global_anniversary').css('display','block');
        $('#gallery_birthday, .global_birthday').css('display','none');
        $('#gallery_celebrate, .global_celebrate').css('display','none');
        $('#gallery_honour, .global_honour').css('display','none');
        $('#no_image').css('display','none');
    }else if(images_recieved[0] == 'Birthday'){
        $('button.birthday_tablink').css({'color':'#fff','background-color': '#00b1b3', 'font-size': '15px'})
        $('#gallery_announcement, .global_announcement').css('display','none');
        $('#gallery_anniversary, .global_anniversary').css('display','none');
        $('#gallery_birthday, .global_birthday').css('display','block');
        $('#gallery_celebrate, .global_celebrate').css('display','none');
        $('#gallery_honour, .global_honour').css('display','none');
        $('#no_image').css('display','none');
    }else if(images_recieved[0] == 'Honour'){
        $('button.honour_tablink').css({'color':'#fff','background-color': '#00b1b3', 'font-size': '15px'})
        $('#gallery_announcement, .global_announcement').css('display','none');
        $('#gallery_anniversary, .global_anniversary').css('display','none');
        $('#gallery_birthday, .global_birthday').css('display','none');
        $('#gallery_celebrate, .global_celebrate').css('display','none');
        $('#gallery_honour, .global_honour').css('display','block');
        $('#no_image').css('display','none');
    }else{
        $('button.celebrate_tablink').css({'color':'#fff','background-color': '#00b1b3', 'font-size': '15px'})
        $('#gallery_announcement, .global_announcement').css('display','none');
        $('#gallery_anniversary, .global_anniversary').css('display','none');
        $('#gallery_birthday, .global_birthday').css('display','none');
        $('#gallery_celebrate, .global_celebrate').css('display','block');
        $('#gallery_honour, .global_honour').css('display','none');
        $('#no_image').css('display','none');
    }

    isImageshere()
    /*$('button.annouce_tablink .badge').css('display', 'inline-block');
    $('button.annouce_tablink .badge').text(data_storage['image_paths']['announcement'].length)
    $('button.anniversary_tablink .badge').css('display', 'none');
    $('button.birth_tablink .badge').css('display', 'none');*/

});

var data_storage = JSON.parse(my_storage);

/* ################################################################ Tab Movement ################################################################ */
function moveReport(evt, tabname){
    var iter, tabcontent, tablinks;
    $('#no_image').css('display','none');
    if(tabname == 'gallery_announcement'){
        $('#gallery_announcement, .global_announcement').css('display','block');
        $('#gallery_anniversary, .global_anniversary').css('display','none');
        $('#gallery_birthday, .global_birthday').css('display','none');
        $('#gallery_celebrate, .global_celebrate').css('display','none');
        $('#gallery_honour, .global_honour').css('display','none');

        $('button.annouce_tablink').css({'color':'#fff','background-color': '#00b1b3', 'font-size': '15px', 'font-weight': '600'})
        $('button.anniversary_tablink').css({'color':'#000','background-color': 'transparent', 'font-size': '13px', 'font-weight': '600'})
        $('button.birth_tablink').css({'color':'#000','background-color': 'transparent', 'font-size': '13px', 'font-weight': '600'})
        $('button.celebrate_tablink').css({'color':'#000','background-color': 'transparent', 'font-size': '13px', 'font-weight': '600'})
        $('button.honour_tablink').css({'color':'#000','background-color': 'transparent', 'font-size': '13px', 'font-weight': '600'})

       /* $('button.annouce_tablink .badge').css('display', 'inline-block');
        $('button.annouce_tablink .badge').text(data_storage['image_paths']['announcement'].length)
        $('button.anniversary_tablink .badge').css('display', 'none');
        $('button.birth_tablink .badge').css('display', 'none');*/

    }else if(tabname == 'gallery_anniversary'){
        $('#gallery_announcement, .global_announcement').css('display','none');
        $('#gallery_anniversary, .global_anniversary').css('display','block');
        $('#gallery_birthday, .global_birthday').css('display','none');
        $('#gallery_celebrate, .global_celebrate').css('display','none');
        $('#gallery_honour, .global_honour').css('display','none');

        $('button.annouce_tablink').css({'color':'#000','background-color': 'transparent', 'font-size': '13px', 'font-weight': '600'})
        $('button.anniversary_tablink').css({'color':'#fff','background-color': '#00b1b3', 'font-size': '15px', 'font-weight': '600'})
        $('button.birth_tablink').css({'color':'#000','background-color': 'transparent', 'font-size': '13px', 'font-weight': '600'})
        $('button.celebrate_tablink').css({'color':'#000','background-color': 'transparent', 'font-size': '13px', 'font-weight': '600'})
        $('button.honour_tablink').css({'color':'#000','background-color': 'transparent', 'font-size': '13px', 'font-weight': '600'})

        /*$('button.annouce_tablink .badge').css('display', 'none');
        $('button.anniversary_tablink .badge').css('display', 'inline-block');
        $('button.anniversary_tablink .badge').text(data_storage['image_paths']['anniversary'].length)
        $('button.birth_tablink .badge').css('display', 'none');*/

    }else if(tabname == 'gallery_birthday'){
        $('#gallery_announcement, .global_announcement').css('display','none');
        $('#gallery_anniversary, .global_anniversary').css('display','none');
        $('#gallery_birthday, .global_birthday').css('display','block');
        $('#gallery_celebrate, .global_celebrate').css('display','none');
        $('#gallery_honour, .global_honour').css('display','none');

        $('button.annouce_tablink').css({'color':'#000','background-color': 'transparent', 'font-size': '13px', 'font-weight': '600'})
        $('button.anniversary_tablink').css({'color':'#000','background-color': 'transparent', 'font-size': '13px', 'font-weight': '600'})
        $('button.birth_tablink').css({'color':'#fff','background-color': '#00b1b3', 'font-size': '15px', 'font-weight': '600'})
        $('button.celebrate_tablink').css({'color':'#000','background-color': 'transparent', 'font-size': '13px', 'font-weight': '600'})
        $('button.honour_tablink').css({'color':'#000','background-color': 'transparent', 'font-size': '13px', 'font-weight': '600'})

        /*$('button.annouce_tablink .badge').css('display', 'none');
        $('button.anniversary_tablink .badge').css('display', 'none');
        $('button.birth_tablink .badge').css('display', 'inline-block');
        $('button.birth_tablink .badge').text(data_storage['image_paths']['birthday'].length)*/

    }else if(tabname == 'gallery_honour'){
        $('#gallery_announcement, .global_announcement').css('display','none');
        $('#gallery_anniversary, .global_anniversary').css('display','none');
        $('#gallery_birthday, .global_birthday').css('display','none');
        $('#gallery_honour, .global_honour').css('display','block');
        $('#gallery_celebrate, .global_celebrate').css('display','none');

        $('button.annouce_tablink').css({'color':'#000','background-color': 'transparent', 'font-size': '13px', 'font-weight': '600'})
        $('button.anniversary_tablink').css({'color':'#000','background-color': 'transparent', 'font-size': '13px', 'font-weight': '600'})
        $('button.birth_tablink').css({'color':'#000','background-color': 'transparent', 'font-size': '13px', 'font-weight': '600'})
        $('button.honour_tablink').css({'color':'#fff','background-color': '#00b1b3', 'font-size': '15px', 'font-weight': '600'})
        $('button.celebrate_tablink').css({'color':'#000','background-color': 'transparent', 'font-size': '13px', 'font-weight': '600'})

    }else{
        $('#gallery_announcement, .global_announcement').css('display','none');
        $('#gallery_anniversary, .global_anniversary').css('display','none');
        $('#gallery_birthday, .global_birthday').css('display','none');
        $('#gallery_honour, .global_honour').css('display','none');
        $('#gallery_celebrate, .global_celebrate').css('display','block');

        $('button.annouce_tablink').css({'color':'#000','background-color': 'transparent', 'font-size': '13px', 'font-weight': '600'})
        $('button.anniversary_tablink').css({'color':'#000','background-color': 'transparent', 'font-size': '13px', 'font-weight': '600'})
        $('button.birth_tablink').css({'color':'#000','background-color': 'transparent', 'font-size': '13px', 'font-weight': '600'})
        $('button.honour_tablink').css({'color':'#000','background-color': 'transparent', 'font-size': '13px', 'font-weight': '600'})
        $('button.celebrate_tablink').css({'color':'#fff','background-color': '#00b1b3', 'font-size': '15px', 'font-weight': '600'})
    }
}
/* ################################################################ Tab Movement ################################################################ */


// ######################### modified images ########################################

function openModal(){
    if($('#popup_image') != null){
        $("#popup_image").hide().fadeIn(1000);
        $('#popup_image').css('display','block');
    }
}

var slideIndex = 1;
showSlides(slideIndex);

function plusSlides(n){
    if(n == 37){n = -1}
    else if(n == 39){n = 1}
    showSlides(slideIndex += n);
}

function currentSlide(event){
    n = parseInt($(event).attr('value'))
    if(n == 37){n = -1}
    else if(n == 39){n = 1}
    showSlides(slideIndex = n);
}

function showSlides(n){
    announce_tag = $('#popup_image .global_announcement').attr('style')
    anni_tag = $('#popup_image .global_anniversary').attr('style')
    birth_tag = $('#popup_image .global_birthday').attr('style')
    celebrate_tag = $('#popup_image .global_celebrate').attr('style')
    honour_tag = $('#popup_image .global_honour').attr('style')
    if(announce_tag != undefined && announce_tag.includes("block") == true){
        var slides = $('.global_announcement .mySlides');
    }else if(anni_tag != undefined && anni_tag.includes("block") == true){
        var slides = $('.global_anniversary .mySlides');
    }else if(birth_tag != undefined && birth_tag.includes("block") == true){
        var slides = $('.global_birthday .mySlides');
    }else if(honour_tag != undefined && honour_tag.includes("block") == true){
        var slides = $('.global_honour .mySlides');
    }else{
        var slides = $('.global_celebrate .mySlides');
    }
    var i;
    if (n > slides.length){slideIndex = 1}
    if (n < 1){slideIndex = slides.length}
    for (i = 0; i < slides.length; i++) {
      slides[i].style.display = "none";
    }
    if(slides.length != 0){
        slides[slideIndex-1].style.display = "block";
    }
}
// ######################### modified images #######################################


function isImageshere(){
    let check_image = 0
    $.each(data_storage['template_image_path'], function(key_, value_){
        if(value_.length == 0){
            check_image = check_image + value_.length
            if(key_ == 'Announcement'){$('.annouce_tablink').css('display', 'none');}
            else if(key_ == 'Anniversary'){$('.anniversary_tablink').css('display', 'none');}
            else if(key_ == 'Birthday'){$('.birth_tablink').css('display', 'none');}
            else if(key_ == 'Celebration'){$('.celebrate_tablink').css('display', 'none');}
            else if(key_ == 'Honour'){$('.honour_tablink').css('display', 'none');}
        }else{
            check_image = check_image + value_.length
        }
    })
    if(check_image == 0){
        $('#no_image').css('display','block');
    }else{
        $('#no_image').css('display','none');
    }
}

