from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ...models import Course, Task, TaskOrder


@csrf_exempt
def tasks_list(request, id):
    if request.user.is_superuser:
        try:
            course = Course.objects.get(id=id)
        except Course.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Course not found'
            }, status=404)
                       
        if request.method == 'GET':
            # tasks = course.tasks.order_by('taskorder__order')
            task_orders = TaskOrder.objects.filter(course_id=id).order_by('order')
            tasks = [task_order.task for task_order in task_orders]
        
            if len(tasks) > 0:
                data = [{
                    'id': task.id, 
                    'title': task.title, 
                    'type': task.type,
                    'public': task.public,
                    'updated': task.updated.strftime("%Y.%m.%d"),
                    'created': task.created.strftime("%Y.%m.%d"),
                } for task in tasks]
                
                return JsonResponse({
                    'size': len(tasks),
                    'tasks': data   
                }, safe=False)
            else:
                return JsonResponse({
                    'status': 'success',
                    'message': 'Tasks not found'
                })
    else:
        return JsonResponse({
            'status': 'Error',
            'message': 'User is not a superuser'
        }, status=403)


@csrf_exempt
def change_task_place(request, id, task_id, new_order):
    if request.user.is_superuser:
        try:
            course = Course.objects.get(id=id)
            task = Task.objects.get(id=task_id)
            order_1 = TaskOrder.objects.get(course=course, task=task)
            order_2 = TaskOrder.objects.get(course=course, task=new_order)
            
        except (Course.DoesNotExist, Task.DoesNotExist, TaskOrder.DoesNotExist):
            return JsonResponse({
                'status': 'error',
                'message': 'Course or Task not found'
            }, status=404)

        if request.method == 'POST': # Assuming you'll send the new order via POST
            print(task_id, new_order)
            print('Model 1',order_1, 'Place 1', order_1.order,'Model 2', order_2, 'Place 2', order_2.order)
            
            if new_order is not None:
                # order.order = new_order
                order1_place = order_1.order
                
                order_1.order = order_2.order
                order_2.order = order1_place
                
                order_1.save()
                order_2.save()
                
                return JsonResponse({
                    'status': 'success',
                    'message': 'Task order updated successfully'
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'New order not provided'
                })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid request method'
            }, status=405)
    else:
        return JsonResponse({
            'status': 'Error',
            'message': 'User is not a superuser'
        }, status=403)


