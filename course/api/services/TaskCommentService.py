from course.models import TaskComment, Task


def get_comments_without_children_by_task(task: Task) -> [TaskComment]:
    """
        Взятие комментариев без детей

        :param task: Task       - Задание
        :return [TaskComment]   - Список комментариев
    """
    return TaskComment.objects.prefetch_related("task_comment_children").filter(task=task,
                                                                                task_comment_parent=None)