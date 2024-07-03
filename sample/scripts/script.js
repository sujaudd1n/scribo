const btn = document.querySelector('.header__nav_toggle');
const nav = document.querySelector('.header__nav');

btn.addEventListener("click", toggle_nav)

function toggle_nav() {
    if (btn.classList.contains("hidden")) {
        btn.classList.replace('ri-menu-line', 'ri-close-line')
    }
    else {
        btn.classList.replace('ri-close-line', 'ri-menu-line')
    }
    btn.classList.toggle("hidden")
    nav.classList.toggle("show")
}

