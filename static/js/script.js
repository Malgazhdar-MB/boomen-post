//var navbar = document.getElementById("")
var content = document.getElementById("content");
$(document).ready(function () {

    $('#sidebarCollapse').on('click', function () {
        $('#sidebar').toggleClass('active');
    });
});

console.log('JS file 1.js added successfully!');

// When the user scrolls the page, execute myFunction
//window.onscroll = function() {myFunction()};

// Get the navbar
var sidebar = document.getElementById("sidebar");
// Get the offset position of the navbar
//var sticky = navbar.offsetTop;

// // Add the sticky class to the navbar when you reach its scroll position. Remove "sticky" when you leave the scroll position
// function myFunction() {
//   if (window.pageYOffset >= sticky) {
//     navbar.classList.add("sticky")
//     paragraf.style.marginTop = 80 + 'px'

//   } else {
//     navbar.classList.remove("sticky");
//     paragraf.style.marginTop = 0 + 'px'
//   }
// }