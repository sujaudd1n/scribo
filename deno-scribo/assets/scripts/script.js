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

function set_base_content_padding_bottom() {
    const base_content_el = document.querySelector(".base_content");
    const footer_el = document.querySelector(".footer");
    console.log(footer_el.clientHeight);
    base_content_el.style.paddingBottom = footer_el.offsetHeight + 50 + "px";
}
set_base_content_padding_bottom()

document.addEventListener("DOMContentLoaded", () => {
    const routes_container = document.querySelector(".page_routes summary");
    if (routes_container)
        routes_container.click()
})

document.querySelector(".copyright__year").textContent = new Date().getFullYear();