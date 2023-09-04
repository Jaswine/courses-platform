from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ...models import Course

from ...utils import checking_slug, slug_generator


@csrf_exempt
def courses_list_create(request):
    if request.method == 'GET':
        courses = Course.objects.filter(user=request.user).order_by('-created_at')
        data = [{
                'id': course.id, 
                'title': course.title, 
                'slug': course.slug, 
                'created_at': course.created_at
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
def courses_get_update_delete(request, slug):    
    try:
        course = Course.objects.get(slug=slug)
    except Course.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': f'Course: {slug} not found.'
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