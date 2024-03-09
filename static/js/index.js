function toggleNavbar() {
    const navbar = document.querySelector('.navbar');
    navbar.classList.toggle('active'); 
}

// const navLinks = document.querySelectorAll('.navbar-links a');
// navLinks.forEach(function(link) {
//     link.addEventListener('click', function() {
//         const navbar = document.querySelector('.navbar');
//         navbar.classList.toggle('active');

//         // Optionally, you can add a delay before collapsing the navbar
//         // Adjust the delay time (in milliseconds) based on your preference
//         setTimeout(function() {
//             navbar.style.display = 'none';
//         }, 300);
//     });
// });