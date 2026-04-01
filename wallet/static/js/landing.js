$(document).ready(function(){

    $('.device img').hide();
    $('.slogan h1').hide();
    $('.slogan a').hide();

    setTimeout(function(){
        $('.device img').fadeIn(500);
    }, 500);

    setTimeout(function(){
        $('.diagonal').addClass('diagonal-fix');
        $('.slogan h1').slideDown(500);
        $('.slogan a').fadeIn(700);
    }, 1000);

})