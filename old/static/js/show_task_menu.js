const button = document.querySelector('.task__content__header__show__menu')
const menu = document.querySelector('.task__menu')
const close = document.querySelector('.task__menu__close')

button.addEventListener('click', () => {
   menu.style.display = 'block';
   setTimeout(() => {
      menu.style.left = '0'
   }, 100)
})

close.addEventListener('click', () => {
   menu.style.left = '-100%'
   setTimeout(() => {
      menu.style.display = 'block';
   }, 100)
});