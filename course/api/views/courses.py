from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from datetime import datetime

from ...models import Course, CourseReview, TaskOrder, TaskComment
from ..utils import get_element_or_404

@csrf_exempt
def courses_list_create(request):
    if request.method == 'GET':
        query = request.GET.get('q', '')
        courses = Course.objects.all().order_by('-updated')
        
        order_by_date = request.GET.get('order_by_data', '-updated')
        order_by_popular = request.GET.get('order_by_popular', 'popular')
        filter_by_tag = request.GET.get('filter_by_tag', '')
        
        if order_by_date is not None and order_by_date != '':
            if order_by_date == 'Oldest':
                courses = Course.objects.all().order_by('created')
            elif order_by_date == 'Newest':
                courses = Course.objects.all().order_by('-created')
     
        if order_by_popular is not None and order_by_popular != '':
            if order_by_popular == 'Unpopular':
                courses = Course.objects.annotate(n=Count('likes')).order_by('-n')                
            else:
                courses = Course.objects.annotate(n=Count('likes')).order_by('n')
                
        if filter_by_tag is not None and filter_by_tag != '':
            if filter_by_tag == 'All':
                courses = Course.objects.all().order_by('-updated')
            else:
                courses = Course.objects.filter(tags__name__icontains=filter_by_tag)
                
        if query:
            courses =  Course.objects.filter(title__icontains=query).order_by('-updated')
                
        data = [{
                'id': course.id, 
                'title': course.title, 
                'user': course.user.username,
                'tags': [{'id': tag.id, 'name': tag.name} for tag in course.tags.all()],
                'image': course.image.url if course.image else None,
                'likes': course.likes.count(),
                'comments_count': CourseReview.objects.filter(course=course).count(),
                'liked_for_this_user':True if request.user in course.likes.all() else False,
                'updated': course.updated.strftime("%Y.%m.%d"),
                'created': course.created.strftime("%Y.%m.%d"),
                } for course in courses]
        
        return JsonResponse({
            'size': courses.count(),
            'courses': data   
        }, safe=False)

    elif request.method == 'POST':
        if request.user.is_superuser:
            title = request.POST.get('title')
        
            course = Course.objects.create( 
                title = title,
            )
            
            course.user.add(request.user)
            
            data = {'id': course.id, 
                    'slug': course.slug }
            
            return JsonResponse(data, status=201)
        
        return JsonResponse({
            'status': 'error',
            'message': 'Dragon Ban: Not even a dragon can fly here. Access is denied.'
        }, status=403)
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Access denied for this method: This method seems to be illegal in this world.'
        }, status=405)
   
@csrf_exempt
def courses_get_update_delete(request, id):    
    course = get_element_or_404(Course, id)
    if isinstance(course, JsonResponse):
        return course
        
    if request.user.is_superuser:
        if request.method == 'GET':
            response_data = dict()

            response_data['title'] = course.title
            response_data['user_registered'] =  True if request.user in course.users_who_registered.all() else False

            lessons_count, videos_count, exercises_count, projects_count = 0, 0, 0, 0

            for title in course.course_titles.all():
                for task in title.tasks.all():
                    lessons_count += 1
                    if task.type == 'TaskVideo':
                        videos_count += 1
                    elif task.type == 'TaskProject':
                        projects_count += 1
                    elif task.type == 'TaskQuestions' or task.type == 'TaskCode':
                        exercises_count += 1

            response_data['lessons_count'] = lessons_count
            response_data['videos_count'] = videos_count
            response_data['exercises_count'] = exercises_count
            response_data['projects_count'] = projects_count

            return JsonResponse({
                'status': 'success',
                'data': response_data
            }, status=200)
        if request.method == 'PUT':
            course.title = request.POST.get('title', '')
            course.image = request.FILES.get('image', '')
            course.about = request.POST.get('about', '')
            course.save()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Course was successfully updated'
            }, status=404)
        elif request.method == 'DELETE':
            return JsonResponse({
                'status': 'success',
                'message': 'Course was successfully deleted'
            }, status=404)
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Access denied for this method: This method seems to be illegal in this world.'
            }, status=405)
    else:
        return JsonResponse({
            'status': 'error',
            'message': "Only brothers of the Night's Watch can pass. You will have to find another way."
        }, status=403)
    
@csrf_exempt
def course_show_tasks(request, id):
    course = get_element_or_404(Course, id)
    if isinstance(course, JsonResponse):
        return course

    if request.method == 'GET':
        task_orders = TaskOrder.objects.filter(course_id=id).order_by('order')
        tasks_all = [task_order.task for task_order in task_orders]
        
        completed_tasks_count = 0
        tasks = []
        
        for index,task in enumerate(tasks_all):
            if task.public:
                status = 'Yes' if request.user in task.users_who_completed.all() else 'No' if request.user.is_authenticated else ''
                if status == 'Yes':
                    completed_tasks_count += 1

                tasks.append({
                    "id": index+1,
                    "title": task.title,
                    "type": task.type,
                    "status": status,
                })
        videos_count = sum(1 for task in tasks_all if task.type == 'video')
        tasks_len = len(tasks)

        return JsonResponse({
            'course': course.title,
            'completed': completed_tasks_count * 100 / tasks_len,
            'tasks_count': tasks_len,
            'videos_count': videos_count,
            'tasks': tasks,
        })
    
@csrf_exempt
def course_add_like(request, id):
    course = get_element_or_404(Course, id)
    if isinstance(course, JsonResponse):
        return course
    
    if request.user.is_authenticated:
    
        if request.method == 'POST':
            if request.user in course.likes.all():
                course.likes.remove(request.user)
                
                return JsonResponse({
                    'status': 'success',
                    'message': 'User like removed successfully'
                }, status=200)
            else:
                course.likes.add(request.user)
            
                return JsonResponse({
                    'status': 'success',
                    'message': 'Course was liked successfully'
                }, status=200)
    else:
        return JsonResponse({
            'status': 'error',
            'message': f'User unauthenticated!'
        }, status=401)
        
@csrf_exempt
def user_add_to_course(request, id):
    course = get_element_or_404(Course, id)
    if isinstance(course, JsonResponse):
        return course
    
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.user in course.users_who_registered.all():
                course.users_who_registered.remove(request.user)
                course.save()
                
                return JsonResponse({
                    'status': 'success',
                    'message': 'Course was removed from user profile successfully'
                }, status=200)
            else:
                course.users_who_registered.add(request.user)
                course.save()
                
                return JsonResponse({
                    'status': 'success',
                    'message': 'Course was added to user profile successfully'
                }, status=200)
    else:
        return JsonResponse({
            'status': 'error',
            'message': f'User unauthenticated!'
        }, status=401)
        
        
def course_reviews_show_create(request, id):
    course = get_element_or_404(Course, id)
    if isinstance(course, JsonResponse):
        return course
        
    if request.method == 'GET':
        reviews = CourseReview.objects.filter(course=course).order_by('-created')
        medium__stars = 0
        
        for review in reviews:
            medium__stars += review.stars
        
        medium__stars = medium__stars / len(reviews) if len(reviews) > 0 else 0
        
        data = [{
            'id': review.id,
            'message': review.message,
            'stars': review.stars,
            'user': {
                'id': review.user.id,
                'username': review.user.username,
                'image': 'https://images.unsplash.com/photo-1696509528129-c28dc0308733?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2663&q=80',
            },
            'updated': datetime.fromisoformat(str(review.updated).replace("Z", "+00:00")).strftime("%d.%m.%Y %H:%M")
        } for review in reviews]
        
        if len(reviews) > 0:
            return JsonResponse({
                'status': 'success',
                'medium__stars': round(medium__stars, 2),
                'data': data
            }, status=200)
        else:
            return JsonResponse({
                'status': 'success',
                'medium__stars':0,
            }, status=200)
            
    elif request.method == 'POST':
        if request.user.is_authenticated:
            message = request.POST.get('message')
            stars_count = request.POST.get('stars_count')
            print('message', message, stars_count)
            
            if stars_count and message:
                review = CourseReview.objects.create(
                    user = request.user,
                    course = course,
                    message = message,
                    stars = stars_count
                )
                
                return JsonResponse({
                    'status': 'success',
                    'message': 'Review created successfully'    
                }, status=201)
            return JsonResponse({
                    'status': 'error',
                    'message': 'You need to choose some stars and write message'    
            }, status=400)
        else:
            return JsonResponse({
                'status': 'error',
                'message': "No White Walkers allowed"
            }, status=401)
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Access denied for this method: This method seems to be illegal in this world.'
        })
    
@csrf_exempt    
def course_reviews_delete(request, id):
    review = get_element_or_404(CourseReview, id)
    if isinstance(review, JsonResponse):
        return review
        
    if request.user.id == review.user.id:
        if request.method == 'DELETE':
            review.delete()
            
            return JsonResponse({
                'status': 'error',
                'message': f'Review with id {id} deleted successfully'
            })
        
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Access denied for this method: This method seems to be illegal in this world.'
            })
           
    return JsonResponse({
        'status': 'error',
        'message': 'You can try, but this place is locked tighter than the Iron Throne.'
    }, status=403) 
