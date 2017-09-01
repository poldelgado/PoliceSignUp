function checkScroll(){
    var startY = $('.navbar').height() * 2; //The point where the navbar changes in px

    if($(window).scrollTop() < startY){
        $('.navbar').addClass("navbar-transparent");
    }else{
        $('.navbar').removeClass("navbar-transparent");
        }
    }