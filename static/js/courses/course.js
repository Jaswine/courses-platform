import { createGlobalMessage } from './globalMessage.js'
import {complaintGlobalWindow} from "./complaint_global_window.js";
import {confirmGlobalWindow} from "./confirm_global_window.js";
import {showHideElement} from "./show_hide_element.js";


document.addEventListener('DOMContentLoaded', () => {
      const UserId = document.querySelector('#UserId')
      const CourseId = document.querySelector('#CourseId').value
      const TasksContent = document.querySelector('#TasksContent')
      const enrollDropInACourse = document.querySelector('#enrollDropInACourse')
      var courseRegisterStatus = false
      let reviewSentStatus = true

      const CourseLessonsCount = document.querySelector('#CourseLessonsCount')
      const CourseVideosCount = document.querySelector('#CourseVideosCount')
      const CourseExerciesesCount = document.querySelector('#CourseExerciesesCount')
      const CourseProjectsCount = document.querySelector('#CourseProjectsCount')
      const CourseHeaderExperienceLine = document.querySelector('#CourseHeaderExperienceLine')
      const courseReviewsForm = document.querySelector('#CourseReviewsForm')
      const CourseReviewsList = document.querySelector('#CourseReviews')
      const reviewStarsCount = document.querySelector('#ReviewStarsCount')


      const fetchCourseInfo = async () => {
            const response = await fetch(`/api/courses/${CourseId}`)
            const data = await response.json()

            if (data.status === 'success') {
                  RenderButtons(data.data.user_registered)
                  RenderCourseInfo(data.data)
                  renderTitleTasks(data.data.titles)
                  console.log(data.data)
            }
      }

      const RenderButtons = (user_registered) => {
            courseRegisterStatus = user_registered
            let courseContinue = document.querySelector('#CourseContinue')
            courseContinue.href = `/courses/${CourseId}/`

            if (courseRegisterStatus) {
                  enrollDropInACourse.classList.remove('btn')
                  enrollDropInACourse.innerHTML = 'Drop'

                  courseContinue.style.display = 'block'
            } else {
                  enrollDropInACourse.classList.add('btn')
                  enrollDropInACourse.innerHTML = 'Enroll in a course'

                  courseContinue.style.display = 'none'
            }
      }

      const RenderCourseInfo = (data) => {
            CourseLessonsCount.innerHTML = `${data.lessons_count} Lessons`
            CourseVideosCount.innerHTML = data.videos_count + " Videos"
            CourseExerciesesCount.innerHTML = data.exercises_count + " Exercises"
            CourseProjectsCount.innerHTML = data.projects_count + " Projects"

            if (data.completed_tasks_count && data.lessons_count) {
                  let completed_precent = data.completed_tasks_count * 100 / data.lessons_count
                  CourseHeaderExperienceLine.style.width = completed_precent + '%'
            } else {
                  CourseHeaderExperienceLine.style.width = 0
            }

            if (data.lessons_count !== data.completed_tasks_count) {
                  courseReviewsForm.innerHTML = ''
                  courseReviewsForm.style.display = 'none'
            }
      }

      const renderTitleTasks = (titles) => {
            TasksContent.innerHTML = '<h2>📑 Course Program</h2>'
            titles.forEach(title => {
                  renderTitle(title)
            });
      }

      const renderTitle = (title) => {
            if (title.public) {
                  const div = document.createElement('div')
                  div.classList.add('tasks__title')

                  const div_header = document.createElement('div')
                  div_header.classList.add('tasks__title__header')

                  const div_h3 = document.createElement('h4')
                  div_h3.innerHTML = title.title
                  div.appendChild(div_h3)

                  div_header.appendChild(div_h3)
                  div.appendChild(div_header)

                  title.tasks.forEach((task, index) => {
                        const div_task = document.createElement('div')
                        div_task.classList.add('task')

                        const div_task__right = document.createElement('div')
                        div_task__right.classList.add('task__left')

                        if (task.completed_status) {
                              const div_task_type = document.createElement('span')
                              div_task_type.classList.add('task__done')
                              task.completed_status == 'Completed' ?
                                    div_task_type.style.backgroundColor = 'rgb(234, 182, 225)' :
                                    div_task_type.style.backgroundColor = 'transparent'
                              div_task__right.appendChild(div_task_type)
                        }

                        let image_type = ""
                        switch (task.type) {
                              case "TaskVideo":
                                    image_type = "<i class='fa-solid fa-clapperboard'></i>"
                                    break
                              case "TaskProject":
                                    image_type = "<i class='fa-solid fa-briefcase'></i>"
                                    break
                              case "TaskQuestions":
                                    image_type = "<i class='fa-solid fa-file-circle-question'></i>"
                                    break
                              case "TaskCode":
                                    image_type = "<i class='fa-solid fa-file-code'></i>"
                                    break
                              default:
                                    image_type = "<i class='fa-solid fa-file-lines'></i>"
                        }

                        div_task__right.innerHTML += image_type

                        const div_task_type_a = document.createElement('a')
                        div_task_type_a.innerHTML = task.title
                        task.completed_status ? div_task_type_a.href=`/courses/${CourseId}/${task.id}/` : ''
                        div_task__right.appendChild(div_task_type_a)

                        const div_task__left = document.createElement('div')
                        div_task__left.classList.add('task__right')
                        div_task__left.innerHTML = `
                              <a ${task.completed_status ? `href='/courses/${CourseId}/${task.id}/'` : ''}>
                                    <svg width="13.25" height="23.75" viewBox="0 0 13.25 23.75" fill="none" xmlns="http://www.w3.org/2000/svg">
                                          <path d="M1.26761 1.25L11.8734 11.8558" stroke="#202020" stroke-width="2.5" stroke-linecap="round"/>
                                          <path d="M1.25 22.4146L11.8558 11.8088" stroke="#202020" stroke-width="2.5" stroke-linecap="round"/>
                                    </svg>
                              </a>
                        
                        `

                        div_task.appendChild(div_task__right)
                        div_task.appendChild(div_task__left)

                        div.appendChild(div_task)
                  })

                  TasksContent.appendChild(div)
            }
      }

      fetchCourseInfo()

      enrollDropInACourse.addEventListener('click', () => {
            fetch(`/api/courses-like/${CourseId}/add-to-course`, {
                  method: 'POST',
              })
                  .then(response => response.json())
                  .then(() => {
                        courseRegisterStatus ? RenderButtons(false) : RenderButtons(true)
                        fetchCourseInfo()
                        getReviews()
                  })
                  .catch(error => {
                        console.log(error.message)
                  })
      })

      const ratingStars = [...document.querySelectorAll(".course__review__form__bottom__rating__star")];
      let starsCount = 0

      function executeRating(stars) {
        const starClassActive = "course__review__form__bottom__rating__star star__pink fas fa-star";
        const starClassInactive = "course__review__form__bottom__rating__star far fa-star";
        const starsLength = stars.length;
        let i;
        stars.map((star) => {
          star.onclick = () => {
            i = stars.indexOf(star);

            if (star.className===starClassInactive) {
              starsCount = 0
              for (i; i >= 0; --i) {
                    starsCount += 1
                    stars[i].className = starClassActive
              }
            } else {
              starsCount += 1
              for (i; i < starsLength; ++i) {
                    starsCount -= 1
                    stars[i].className = starClassInactive
              }
            }
          };
        });
      }

      executeRating(ratingStars);

      const getReviews = async () => {
            const response = await fetch(`/api/courses/${CourseId}/reviews`)
            const data = await  response.json()

            if (data.status === 'success') {
                let comment_stars = ''
                for (let i = 1; i <= Math.round(data.data.medium__stars); i++) {
                    comment_stars += '<span class="comment_item__header__left__star fas fa-star"></span>'
                }

                reviewStarsCount.innerHTML = `
                    <div class="course__reviews__filters__main__number">${data.data.medium__stars}</div>
                    <div class="course__review__form__bottom__rating">${comment_stars}</div>
                `

                renderCourseReviews(CourseReviewsList, data.data.reviews)

                if (reviewSentStatus) {
                    courseReviewsForm.style.display = 'flex'
                }
            }
      }

      const renderCourseReviews = (list, comments) => {
          list.innerHTML = ''
          ReviewListCount.innerHTML = comments.length + ' reviews'

          comments.forEach(comment => {
              const taskCommentElement = renderCourseReview(comment);
              list.appendChild(taskCommentElement);
          });
      }

       const renderCourseReview = (comment) => {
          const div = document.createElement('div');
          div.classList.add('comment_item');
          div.id = `comment-${comment.id}`;

          if (comment.user.id == UserId.value) {
              reviewSentStatus = false
          }

          const div_header = document.createElement('div');
          div_header.classList.add('comment_item__header');

          const div_header_left = document.createElement('div');
          div_header_left.classList.add('comment_item__header__left');
          div_header_left.innerHTML += `<img src="${comment.user.ava ? comment.user.ava : '/static/index/ava.jpg'}" alt="${comment.user.username}" />`;
          div_header_left.innerHTML += `<a href="/users/${comment.user.username}">${comment.user.username}</a>`
          div_header_left.innerHTML += ` - `

          let comment_stars = ``
          for (let i = 1; i <= Math.round(comment.stars); i++) {
            comment_stars += '<span class="comment_item__header__left__star fas fa-star"></span>'
          }
          console.log('comment stars: ', comment_stars)
          div_header_left.innerHTML += `<div class="course__review__form__bottom__rating">${comment_stars}</div>`;

          const div_header_right = document.createElement('img');
          div_header_right.classList.add('comment_item__header__icon');
          div_header_right.src = '/static/icons/MenuVertical.svg';
          div_header_right.alt = 'MenuVertical';

          const div_header_right_menu = document.createElement('div');
          div_header_right_menu.classList.add('comment_item__header__menu');
          div_header_right_menu.style.opacity = 0;
          div_header_right_menu.style.display = 'none';

          if (UserId && UserId.value == comment.user.id) {
              const delete_comment_button = document.createElement('div');
              delete_comment_button.innerHTML = `<i class="fa-regular fa-trash-can"></i> Delete`;
              div_header_right_menu.appendChild(delete_comment_button);

              delete_comment_button.addEventListener('click', async () => {
                  await confirmGlobalWindow("Do you want to delete this comment?").then(async (confirmed) => {
                      if (confirmed) {
                          await fetch(`/api/courses/reviews/${comment.id}/delete`, {
                              method: 'DELETE',
                          })
                              .then(response => response.json())
                              .then(data => {
                                  createGlobalMessage(data.message);
                                  getReviews()
                              })
                      }
                  });
              });
          }

          showHideElement(div_header_right, div_header_right_menu);

          div_header.appendChild(div_header_left);
          div_header.appendChild(div_header_right);
          div_header.appendChild(div_header_right_menu);
          div.appendChild(div_header);

          // Create comment's text
          const div_text = document.createElement('div');
          div_text.classList.add('comment_item__text');
          div_text.innerHTML = comment.message;
          div.appendChild(div_text);

          // Create comment's footer
          const div_footer = document.createElement('div');
          div_footer.classList.add('comment_item__footer');

          const div_footer_left = document.createElement('div');
          div_footer_left.classList.add('comment_item__footer__left');

          const div_footer_right = document.createElement('span');
          div_footer_right.innerHTML = comment.created;

          div_footer.appendChild(div_footer_left);
          div_footer.appendChild(div_footer_right);
          div.appendChild(div_footer);

          return div;
      }

      getReviews()

      courseReviewsForm.addEventListener('submit', (e) => {
            e.preventDefault()

            let courseTextArea = courseReviewsForm.querySelector('textarea').value

            if (courseTextArea.length < 6) {
                  createGlobalMessage("Review is too short!")
            } else if (courseTextArea.length > 1000) {
                  createGlobalMessage("Review is too long!")
            } else {
                  if (starsCount && starsCount > 0) {
                        let formData = new FormData(courseReviewsForm)
                        formData.append('stars_count', starsCount)

                        fetch(`/api/courses/${CourseId}/reviews`, {
                              method: 'POST',
                              body: formData,
                        })
                            .then(response => response.json())
                            .then(data => {
                                createGlobalMessage(data.message)
                                 getReviews()
                            })
                  } else {
                    createGlobalMessage("Add some stars!")
                  }
            }
      })
})