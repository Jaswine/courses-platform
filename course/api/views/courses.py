from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from datetime import datetime

from ...models import Course


from ...utils import checking_slug, slug_generator


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
                'image': course.image.url,
                'about': course.about[:150],
                'likes': course.likes.count(),
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