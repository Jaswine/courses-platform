let sliderCount = 0

// Список изображений
const images = [
    { 
        id: 1, 
        image: 'christopher-gower-m_HRfLhgABo-unsplash.jpg', 
        text: 'Welcome to our platform!'
    },
    { 
        id: 2, 
        image: 'faisal-BI465ksrlWs-unsplash.jpg', 
        text: 'Learn something new!'
    },
    { 
        id: 3, 
        image: 'carl-heyerdahl-KE0nC8-58MQ-unsplash.jpg', 
        text: 'Get more experience!'
    },
    { 
        id: 4, 
        image: 'arnel-hasanovic-MNd-Rka1o0Q-unsplash.jpg', 
        text: 'Meet and chat with other people!'
    },
]

document.addEventListener('DOMContentLoaded', () => {
    const left = document.querySelector('.left')
    const right = document.querySelector('.right')

    const slider = document.querySelector('.slider')

    // Рендеринг Слайда
    const renderSlider = (x) => {
        slider.style.opacity = 0
        
        slider.querySelector('.slider__image').src = `/static/media/auth/${images[x].image}`
        slider.querySelector('.slider__count').innerHTML = `${images[x].id}/${images.length}`
        slider.querySelector('.slider__text').innerHTML = images[x].text
        slider.style.opacity = 1
    }

    renderSlider(sliderCount)
 
    left.addEventListener('click', () => {
        renderSlider(
            sliderCount <= 0 ? 
            sliderCount = images.length-1 : 
            sliderCount-- 
        )
    })

    right.addEventListener('click', () => {
        renderSlider(
            sliderCount > images.length-1 ? 
            sliderCount = 0 : 
            sliderCount++ 
        )
    })
})  