$(document).ready(function(){

    $('.device img').hide();

    setTimeout(function(){
        $('.device img').fadeIn(500);
    }, 500);

    setTimeout(function(){
        $('.diagonal').addClass('diagonal-fix');
    }, 1000);

})