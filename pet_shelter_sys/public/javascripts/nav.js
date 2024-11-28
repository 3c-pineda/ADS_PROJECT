document.addEventListener('DOMContentLoaded', () => {
    const burgerMenu = document.querySelector('.burger-menu');
    const menuItems = document.querySelector('.menu-items');

    burgerMenu.addEventListener('click', () => {
        // Toggle 'menu-active' class on the navigation
        menuItems.classList.toggle('menu-active');
    });
});