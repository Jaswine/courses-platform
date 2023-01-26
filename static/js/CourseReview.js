console.log('CourseReview.js loaded successfully')

const one = document.querySelector('#first');
const two = document.querySelector('#second');
const three = document.querySelector('#third');
const four = document.querySelector('#fourth');
const five = document.querySelector('#fifth');

const review__stars  = document.querySelector('.review__stars');
const starsValue = document.querySelector('#starsValue');
var stars = 0;

// const handleStarsSelect = (stayclass, size) => {
//     const children = review__stars.children
//     for (let i = 0; i < children.length; i++) {
//         if (i<=size) {
//             children[i].classList.add('checked');
//         } else {
//             children[i].classList.remove('checked');
//         }
//     }
// }

// const handleSelected = size => {
//     const children = review__stars.children
//     for (let i = 0; i < children.length; i++) {
//         if (i<=size) {
//             children[i].classList.add('selected');
//         } else {
//             children[i].classList.remove('selected');
//         }
//     }
// }

const handleStarsSelect = (getClasses, stayclases, size) => {
    const children = getClasses.children
    for (let i = 0; i < children.length; i++) {
        if (i<=size) {
            children[i].classList.add(stayclases);
        } else {
            children[i].classList.remove(stayclases);
        }
    }
}

const handleSelect = (selection) => {
    switch(selection) {
        case 'first': {
            handleStarsSelect(review__stars, 'checked', 0)
            return
        }
        case 'second': {
            handleStarsSelect(review__stars, 'checked', 1)
            return
        }
        case 'third': {
            handleStarsSelect(review__stars, 'checked', 2)
            return
        }
        case 'fourth': {
            /*one.classList.add('checked');
            two.classList.add('checked');
            three.classList.add('checked');
            four.classList.add('checked');
            five.classList.remove('checked'); */
            handleStarsSelect(review__stars, 'checked', 3);
            return
        }
        case 'fifth': {
            handleStarsSelect(review__stars, 'checked',4);  
            return 
        }
    }
}

const handleSelectedList = (selection) => {
    switch(selection) {
        case 'first': {
            handleStarsSelect(review__stars, 'selected', 'checked',0);  
            stars = 1
            return
        }
        case 'second': {
            handleStarsSelect(review__stars, 'selected', 'checked',1);  
            stars = 2
            return
        }
        case 'third': {
            handleStarsSelect(review__stars, 'selected', 'checked',2);  
            stars = 3
            return
        }
        case 'fourth': {
            /*one.classList.add('checked');
            two.classList.add('checked');
            three.classList.add('checked');
            four.classList.add('checked');
            five.classList.remove('checked'); */
            handleStarsSelect(review__stars, 'selected', 'checked',3);  
            stars = 4
            return
        }
        case 'fifth': {
            handleStarsSelect(review__stars, 'selected', 'checked',4);  
            stars = 5                              
            return 
        }
    }
}

const arr = [one, two, three, four, five];

console.log(arr);
arr.forEach(item => item.addEventListener('mouseover', (e) => {
    handleSelect(e.target.id);
}));

arr.forEach(item => item.addEventListener('click', (e) => {
    handleSelectedList(e.target.id);
    starsValue.value = stars;
    console.log(starsValue.value);
}));