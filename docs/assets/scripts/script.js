const btn = document.querySelector('.header__nav_toggle');
const nav = document.querySelector('.header__nav');

btn.addEventListener("click", toggle_nav)

function toggle_nav() {
    if (btn.classList.contains("hidden")) {
        btn.classList.replace('ri-menu-line', 'ri-close-line')
        document.body.style.height = "100dvh";
        document.body.style.overflow = "hidden";
    }
    else {
        btn.classList.replace('ri-close-line', 'ri-menu-line')
        document.body.style.height = "auto";
        document.body.style.overflow = "unset";
    }
    btn.classList.toggle("hidden")
    nav.classList.toggle("show")
}
