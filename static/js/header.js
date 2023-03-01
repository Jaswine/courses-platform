const header__menu__icon = document.querySelector(".header__menu__icon");
const header__menu = document.querySelector(".header__menu");

header__menu__icon.onclick = () => {
   if (header__menu.style.top != "60px") {
      header__menu.style.top = "60px"
   }
   header__menu.style.top = "-50vh"
}