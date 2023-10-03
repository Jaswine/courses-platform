document.addEventListener('DOMContentLoaded', () => {
    const line = document.querySelector('.about__content__line__draw')

    const cards = document.querySelectorAll('.card')
    const card__descs = document.querySelectorAll('.card__desc')

    for (let i = 0; i < cards.length; i++) {
        if (i % 2 === 0) {
            cards[i].style.marginLeft = '-15%'
        } else {
            cards[i].style.marginRight = '-15%'
        }
    }

    for (let i = 0; i < card__descs.length; i++) {
        if (i % 2 === 1) {
            card__descs[i].style.marginLeft = '-15%'
        } else {
            card__descs[i].style.marginRight = '-15%'
        }
    }

    window.addEventListener('scroll', (e) => {
        let scrollPosition = window.scrollY;
    
        // Высота контента минус высота окна браузера
        let contentHeight = document.querySelector('.about').offsetHeight;
        let windowHeight = window.innerHeight;
    
        if (scrollPosition > windowHeight / 10 &&  scrollPosition < contentHeight) {
            let scaleHeight = (scrollPosition /  (contentHeight - (windowHeight / 10)) * 100)

            for (let i = 0; i < cards.length; i++) {
                if (i == 0 && scaleHeight > 20) {
                    card__descs[i].style.margin = 0
                    cards[i].style.margin = 0
                } else if (scaleHeight > i * 30 + 20) {
                    card__descs[i].style.margin = 0
                    cards[i].style.margin = 0
                }
            }

            line.style.height = scaleHeight + '%';
        }
    });
})