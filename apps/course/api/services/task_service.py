
from apps.course.api.services.title_service import get_title_order_by_course_id_and_title_id
from apps.course.models import TaskOrder, Task, Title, Course
from apps.user.models import User


def get_tasks_by_title_id(title_id: int) -> list[Task]:
    """
        Взятие заданий у тем курсов по id темы

        :param title_id: int - id темы
        :return list[TaskOrder] - список заданий тем
     """
    tasks_orders = TaskOrder.objects.filter(title_id=title_id).order_by('order')
    return [task_order.task for task_order in tasks_orders]


def get_task_by_id(id: int) -> Task | None:
    """
        Взятие задания по id

        :param id: int - Идентификатор задания
        :return Task | None  - Задание
    """
    try:
        return Task.objects.get(id=id)
    except Task.DoesNotExist:
        return None


def is_user_completed_task(task: Task, user: User) -> bool:
    """
         Проверка регистрации пользователя

         :param task: Task - Задание
         :param user: User - Пользователь
         :return bool - Статус
    """
    return user in task.users_who_completed.all()


def create_task_order(course_title: Title, task: Task) -> TaskOrder | None:
    """
        Создание места для задания

       :param course_title: Title - Тема
       :param task: Task - Задание
       :return TitleOrder | None
   """
    order = course_title.title_tasks.count() + 1
    return TaskOrder.objects.create(title=course_title, task=task, order=order)


def create_task(course_title: Title,
                title: str, task_type: str, points: int):
    """
        Создание задания

        :param course_title: Title - Тема
        :param title: Title - Название
        :param task_type: Task Type - Тип
        :param points: Points  - Очки
    """
    task = Task.objects.create(
        title=title,
        type=task_type,
        points=points,
        public=False
    )

    if task and create_task_order(course_title, task):
        return task
    return task


def update_task(task: Task,
                title: str, public: str, points: int):
    """
        Обновление задания

        :param task: Task - Задание
        :param title: str - Заголовок задания
        :param public: bool - Статус публичности
        :param: points : int -  Колличество очков
    """
    is_changed = False

    if 0 < len(title) < 255:
        task.title = title
        is_changed = True
        task.save()

    if public:
        if public == 'true':
            task.public = False
        else:
            task.public = True
        is_changed = True
        task.save()

    if points:
        task.points = points
        is_changed = True
        task.save()

    return is_changed


def delete_task(task: Task):
    """
        Удалить задание

        :param task: Task - Задание
    """
    task.delete()


def add_remove_task_experience(task: Task, user: User) -> str:
    """
        Добавление / удаление опыта к заданию

        :param task: Task - Задание
        :param user: User - Пользователь
        :return str - Сообщение
    """
    if task.users_who_completed.filter(id=user.id).exists():
        task.users_who_completed.remove(user.id)
        user.scores -= task.points
        user.save()
        return 'Removed task experience successfully!'
    else:
        task.users_who_completed.add(user.id)
        user.scores += task.points
        user.save()
        return 'Added task experience successfully!'


def task_bookmark_is_exists(task: Task, user: User) -> bool:
    """
        Проверка, что закладка существует

        :param task: Task - Задание
        :param user: User - Пользователь
        :return bool - Статус
    """
    return True if user in task.bookmarks.all() else False


def add_remove_task_bookmark(task: Task, user: User) -> str:
    """
        Добавление / удаление задания в закладки

        :param task: Task - Задание
        :param user: User - Пользователь
        :return str - Сообщение
    """
    if user in task.bookmarks.all():
        task.bookmarks.remove(user)
        return 'Bookmark removed successfully!'
    else:
        task.bookmarks.add(user)
        return 'Bookmark added successfully!'


def get_task_order_by_title_id_and_task_id(title_id: int, task_id: int) -> TaskOrder:
    """
        Взятие места задания в списке тем курса

        :param title_id: int - Идентификатор курса
        :param task_id: int - Идентификатор темы курса
        :return TaskOrder - Место темы
    """
    try:
        return TaskOrder.objects.get(title_id=title_id, task_id=task_id)
    except TaskOrder.DoesNotExist:
        return None


def update_tasks_places(task1: Task, task2: Task) -> bool:
    """
        Смена заданий местами

        :param task1: Task - Задание 1
        :param task2: Task - Задание 2
        :return bool - Статус
    """
    try:
        # Retrieve the first TaskOrder object for each task
        task1_order = TaskOrder.objects.filter(task=task1).first()
        task2_order = TaskOrder.objects.filter(task=task2).first()

        if task1_order and task2_order:
            # Swap the order values
            task1_order.order, task2_order.order = task2_order.order, task1_order.order

            # Swap the titles as well if they belong to different titles
            if task1_order.title != task2_order.title:
                task1_order.title, task2_order.title = task2_order.title, task1_order.title

            # Save the updated TaskOrder objects
            task1_order.save()
            task2_order.save()

            return True
        else:
            print("One of the tasks does not have an associated TaskOrder.")
            return False
    except Exception as e:
        print(f"Error swapping tasks: {e}")
        return False
