$(document).ready(function() {
    $("#owl-example").owlCarousel({
    navigation: true, // Show next and prev buttons
    slideSpeed: 300,
    margin: 10,
    paginationSpeed: 400,
    autoplay: false,
    items: 1,
    itemsDesktop: false,
    itemsDesktopSmall: false,
    itemsTablet: false,
    itemsMobile: false,
    loop: true,
    nav: true,
    navText: ["<i class='fa fa-angle-left' aria-hidden='true'></i>", "<i class='fa fa-angle-right' aria-hidden='true'></i>"]
    });
    });