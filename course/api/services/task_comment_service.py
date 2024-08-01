from django.contrib.auth.models import User

from course.forms import TaskCommentUserComplaintForm
from course.models import TaskComment, Task


def get_comments_without_children_by_task(task: Task) -> [TaskComment]:
    """
        Взятие комментариев без детей

        :param task: Task       - Задание
        :return [TaskComment]   - Список комментариев
    """
    return TaskComment.objects.prefetch_related("task_comment_children").filter(task=task,
                                                                                task_comment_parent=None)


def create_task_comment(task: Task, user: User, message: str) -> TaskComment:
    """
        Создание комментария для задания

        :param task: Task - Задание
        :param user: User - Пользователь
        :param message: str - Сообщение
        :return TaskComment - Комментарий к заданию
    """
    return TaskComment.objects.create(
        task=task,
        user=user,
        text=message,
    )


def get_task_comment_by_id(id: int) -> TaskComment:
    """
        Взятие комментария к заданию по идентификатору

        :param id: int - Идентификатор пользователя
        :return TaskComment - Комментарий к заданию
    """
    return TaskComment.objects.get(id=id)


def update_task_comment_parent(task_comment: TaskComment, parent_task_comment: TaskComment) -> TaskComment:
    """
        Обновление родителя комментария

        :param task_comment: TaskComment - Комментарий к заданию
        :param parent_id: int - идентификатор родителя комментария
        :return TaskComment - Комментарий к заданию
    """
    task_comment.task_comment_parent = parent_task_comment
    task_comment.save()

    return task_comment


def delete_task_comment(task_comment: TaskComment):
    """
        Удаление комментария к заданию

        :param task_comment: TaskComment - Комментарий к заданию
    """
    task_comment.delete()


def toggle_like_to_task_comment(task_comment: TaskComment, user: User) -> str:
    """
        Добавление / удаление лайка к комментарию задания

        :param task_comment: Comment    - Статья
        :param user: User          - Пользователь
        :return str                - Сообщение
    """
    if user in task_comment.likes.all():
        task_comment.likes.remove(user)
        return "Like has been removed successfully!"
    else:
        task_comment.likes.add(user)
        return "Like has been added successfully!"


def filter_task_comment_user_complains(comment: TaskComment, user: User) -> [TaskComment]:
    """
        Фильтрация комментариев

        :param comment: TaskComment - Комментарий к заданию
        :param user: User  - Пользователь
        :return [TaskComemnt] - Список комментариев
    """
    return TaskComment.objects.filter(taskComment=comment,
                                      user=user)


def save_task_comment_user_complain_form(comment: TaskComment,
                                         form: TaskCommentUserComplaintForm,
                                         comment_complaints: [TaskComment],
                                         user: User) -> str:
    """
        Создание комментария с помощью формы

        :param comment: TaskComment - Комментарий
        :param form: TaskCommentUserComplaintForm - Форма
        :param comment_complaints: [TaskComment] - Список комментариев
        :param user: User - Пользователь
        :return str - Сообщение
    """
    if form.is_valid() and comment_complaints.count() == 0:
        complaint = form.save(commit=False)
        complaint.taskComment = comment
        complaint.user = user
        complaint.save()

        if comment.complaints.count() >= 10:
            comment.is_public = False
            comment.save()
            return 'Complaint added successfully! The message was hidden as complaints became 10 or more!'
        return 'Complaint added successfully!'
    return form.errors


def task_comment_like_is_exist(task_comment: TaskComment, user: User) -> bool:
    """
        Проверка, что лайк к комментарию задания передаваемого пользователя существует

        :param task_comment: TaskComment - комментарий к заданию
        :param user: User - Пользователь
        :return bool - Статус
    """
    return True if user in task_comment.likes.all() else False


def task_comment_like_count(task_comment: TaskComment) -> int:
    return task_comment.likes.count()