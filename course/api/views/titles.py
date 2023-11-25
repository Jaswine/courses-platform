from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ...models import Course, Title, TitleOrder, TaskOrder, Task
from ..utils import get_element_or_404


@csrf_exempt
def title_list_create(request, id):
    if request.user.is_superuser:
        course = get_element_or_404(Course, id)

        if isinstance(course, JsonResponse):
            return course
        
        if request.method == 'GET':
            titles = course.course_titles.order_by('taskorder__order')
            title_orders = TitleOrder.objects.filter(course_id=id).order_by('order')
            titles = [title_order.title for title_order in title_orders]
            
            if len(titles) > 0:
                data = [{
                    'id': title.id, 
                    'title': title.title, 
                    'public': title.public,
                    'tasks': [task_order for task_order in TaskOrder.objects.filter(title_id=title.id).order_by('order')]
                } for title in titles]
                
                return JsonResponse({
                    'size': len(titles),
                    'titles': data,
                }, safe=False)
            else:
                return JsonResponse({
                    'status': 'success',
                    'message': 'Titles not found'
                })
        elif request.method == 'POST':
            get_title = request.POST.get('title', '')
            if  255 > len(get_title) > 0 :
                title = Title.objects.create(title=get_title)
                title.save()
            
                order = course.course_titles.count() + 1
                TitleOrder.objects.create(course=course, title=title, order=order)
                course.course_titles.add(title)

                return JsonResponse({
                    'status': 'success',
                    'message': ' The subject created successfully!'
                }, status=201)
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': ' The subject cannot be less than 0 or more than 255 characters.'
                }, status=400)
            
        else: 
            return JsonResponse({
                'status': 'error',
                'message': 'Method not allowed'
            }, status=402)
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'User is not a superuser'
        }, status=403)

@csrf_exempt
def title_update_delete(request, id):
    if request.user.is_superuser:
        course_title = get_element_or_404(Title, id)

        if isinstance(course_title, JsonResponse):
            return course_title
        
        if request.method == 'POST':
            title = request.POST.get('title', '')
            public = request.POST.get('public', None)
            is_changed = False

            if 0 < len(title) < 255:
                course_title.title = title
                is_changed = True
                course_title.save()
            
            if public:
                print('public', public)
                if public == 'true':
                    course_title.public = False
                else: 
                    course_title.public = True
                is_changed = True
                course_title.save()

            if is_changed:
                return JsonResponse({
                    'status': 'success',
                    'message': 'Title updated successfully!'
                }, status=200)
            else: 
                 return JsonResponse({
                    'status': 'success',
                    'message': 'Title didn\'t change!'
                }, status=200)
            
        if request.method == 'DELETE':
            course_title.delete()

            return JsonResponse({}, status=204)

        else: 
            return JsonResponse({
                'status': 'error',
                'message': 'Method not allowed'
            }, status=402)

    else:
        return JsonResponse({
            'status': 'error',
            'message': 'User is not a superuser'
        }, status=403)
    
def title_change_place(request, CourseID, TitleID, NewOrder):
    if request.user.is_superuser:
        course = get_element_or_404(Course, CourseID)
        if isinstance(course, JsonResponse):
            return course
        
        title = get_element_or_404(Title, TitleID)
        if isinstance(title, JsonResponse):
            return title
        
        if request.method == 'PUT':
            order_1 = TitleOrder.objects.get(course=course, title=title)
            order_2 = TitleOrder.objects.get(course=course, task=NewOrder)

            if NewOrder is not None:
                order1_place = order_1.order

                order_1.order = order_2.order
                order_2.order = order1_place
                
                order_1.save()
                order_2.save()

                return JsonResponse({
                    'status': 'success',
                    'message': 'Title\' place changed successfully!'
                }, status=200)
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'New order not provided'
                })
        else: 
            return JsonResponse({
                'status': 'error',
                'message': 'Method not allowed'
            }, status=402)
            
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'User is not a superuser'
        }, status=403)