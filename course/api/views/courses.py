from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from datetime import datetime

from ...models import Course, CourseReview

@csrf_exempt
def courses_list_create(request):
    if request.method == 'GET':
        query = request.GET.get('q', '')
        courses = Course.objects.all().order_by('-updated')
        
        order_by_date = request.GET.get('order_by_data', '-updated')
        order_by_popular =  request.GET.get('order_by_popular', 'popular')
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
                'about': course.about[:200],
                'likes': course.likes.count(),
                'liked_for_this_user':True if request.user in course.likes.all() else False,
                'updated': course.updated.strftime("%Y.%m.%d"),
                'created': course.created.strftime("%Y.%m.%d"),
                } for course in courses]
        
        return JsonResponse({
            'size': courses.count(),
            'courses': data   
        }, safe=False)

    elif request.method == 'POST':
        title = request.POST.get('title')
        
        course = Course.objects.create( 
            title = title,
        )
        
        course.user.add(request.user)
        
        data = {'id': course.id, 
                'slug': course.slug }
        return JsonResponse(data, status=201)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
   
@csrf_exempt
def courses_get_update_delete(request, id):    
    try:
        course = Course.objects.get(id=id)
    except Course.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': f'Course: {id} not found.'
        }, status=404)
        
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
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
@csrf_exempt
def course_add_like(request, id):
    try:
        if request.user.is_authenticated:
            course = Course.objects.get(id=int(id))
        
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
        
                
    except Course.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': f'Course: {id} not found.'
        }, status=404)
        
@csrf_exempt
def course_add_(request, id):
    try:
        if request.user.is_authenticated:
            course = Course.objects.get(id=int(id))
        
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
        
                
    except Course.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': f'Course: {id} not found.'
        }, status=404)
        
@csrf_exempt
def user_add_to_course(request, id):
    try:
        if request.user.is_authenticated:
            course = Course.objects.get(id=id)
        
            if request.method == 'POST':
                if request.user in  course.users_who_completed_course.all():
                    course.users_who_completed_course.remove(request.user)
                    course.save()
                    
                    return JsonResponse({
                        'status': 'success',
                        'message': 'Course was removed from user profile successfully'
                    }, status=200)
                else:
                    course.users_who_completed_course.add(request.user)
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
        
                
    except Course.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': f'Course: {id} not found.'
        }, status=404)
        
        
def course_reviews_show_create(request, id):
    try:
        course = Course.objects.get(id=id)
    except Course.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': f'Course with id {id} not found'
        })
        
    if request.method == 'GET':
        reviews = CourseReview.objects.filter(course=course).order_by('-created')
        medium__stars = 0
        
        for review in reviews:
            medium__stars += review.stars
        
        medium__stars = medium__stars / reviews.count()
        
        data = [{
            'id': review.id,
            'message': review.message,
            'stars': review.stars,
            'user': {
                'username': review.user.username,
                'image': 'https://images.unsplash.com/photo-1696509528129-c28dc0308733?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2663&q=80',
            },
            'updated': datetime.fromisoformat(str(review.updated).replace("Z", "+00:00")).strftime("%d.%m.%Y %H:%M")
        } for review in reviews]
        
        return JsonResponse({
            'status': 'success',
            'medium__stars': round(medium__stars, 2),
            'data': data
        }, status=200)
        
    elif request.method == 'POST':
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
            'message': 'Method not supported'
        })
    
@csrf_exempt    
def course_reviews_delete(request, id):
    try:
        review = CourseReview.objects.get(id=id)
    except CourseReview.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': f'Review with id {id} not found'
        })
        
    if request.method == 'DELETE':
        review.delete()
        
        return JsonResponse({
            'status': 'error',
            'message': f'Review with id {id} deleted successfully'
        })
        
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Method not supported'
        })