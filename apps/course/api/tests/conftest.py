from datetime import datetime, timedelta

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from pytest import fixture

from apps.course.models import Tag, Course, CourseReview, Title, Task
from apps.user.models import Profile


@fixture
def tag1(db):
    return Tag.objects.create(name='Tag1')


@fixture
def tag2(db):
    return Tag.objects.create(name='Tag2')


@fixture
def tag_list(db, tag1, tag2):
    return [tag1, tag2]


@fixture
def user_is_superuser(db):
    user = User.objects.create(username='user1',
                               email='user1@example.com',
                               password=make_password('password'),
                               is_superuser=True)
    Profile.objects.create(user=user)
    return user


@fixture
def user_is_not_superuser(db):
    user = User.objects.create(username='user2',
                               email='user2@example.com',
                               password=make_password('password'))
    Profile.objects.create(user=user)
    return user


# @fixture
# def task(db):
#     return Task.objects.create(title='Task',
#                                type='TaskText',
#                                text='Text',
#                                points=10)


# @fixture
# def task_video(db):
#     return Task.objects.create(title='Video Task',
#                                type='TaskVideo',
#                                video='video.mp4',
#                                points=15)

# @fixture
# def task_project(db):
#     return Task.objects.create(title='Project Task',
#                                type='TaskProject',
#                                points=20)



@fixture
def task_is_public(db, user_is_not_superuser):
    t = Task.objects.create(title='Task',
                               type='TaskText',
                               text='Text',
                               points=10,
                               public=True)
    t.bookmarks.add(user_is_not_superuser)
    t.users_who_completed.add(user_is_not_superuser)
    return t


@fixture
def task_list(db, task, task_is_public):
    return [task, task_is_public]


@fixture
def title(db):
    return Title.objects.create(title='Title')


@fixture
def title_is_public(db):
    return Title.objects.create(title='Title', public=True)


@fixture
def title_list(db, title, title_is_public):
    return [title_is_public, title]


@fixture
def course_is_public(db, user_is_superuser, tag1, user_is_not_superuser, title_is_public):
    course = Course.objects.create(title='Course1',
                                   user=user_is_superuser,
                                   public=True,
                                   image=None,
                                   created=datetime.now() - timedelta(days=2),
                                   updated=datetime.now() - timedelta(days=2))
    course.tags.add(tag1)
    course.likes.add(user_is_not_superuser)
    course.users_who_registered.add(user_is_not_superuser)
    course.course_titles.add(title_is_public)
    return course


@fixture
def course_is_not_public(db, user_is_superuser, tag2):
    course = Course.objects.create(title='Course2',
                                   user=user_is_superuser,
                                   created=datetime.now() - timedelta(days=2),
                                   updated=datetime.now() - timedelta(days=2))
    course.tags.add(tag2)
    return course


@fixture
def course_list(db, course_is_public, course_is_not_public):
    return [course_is_public, course_is_not_public]


@fixture
def course_review(db, user_is_not_superuser, course_is_public):
    return CourseReview.objects.create(
        course=course_is_public,
        user=user_is_not_superuser,
        message='Great course!',
        stars=5,
        created=datetime.now() - timedelta(days=2),
        updated=datetime.now() - timedelta(days=2))


@fixture
def course_review_list(db, course_review):
    return [course_review, course_review]
