from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ...models import Tag

from ...utils import checking_slug, slug_generator


@csrf_exempt
def tags_list_create(request):
    if request.method == 'GET':
        query = request.GET.get('q', '')
        tags =  Tag.objects.all()
        
        if query:
            tags =  Tag.objects.filter(name__icontains=query)
                
        data = [{
                'id': tag.id, 
                'name': tag.name,
                } for tag in tags]
        
        return JsonResponse({
            'status': 'success',
            'tags': data
        }, safe=False)
        
        
    elif request.method == 'POST':
        name = request.POST.get('name', '')
        
        tag = Tag.objects.create( 
            name = name,
        )
                
        data = {'id': tag.id, 
                'name': tag.name }
        return JsonResponse(data, status=201)
    else:
        return JsonResponse({'error': 'Access denied for this method: This method seems to be illegal in this world.'}, status=405)
    
@csrf_exempt
def tags_get_update_delete(request, id):
    try:
        tag = Tag.objects.get(id=id)
    except Tag.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': f'Name tag: {id} not found.'
        }, status=404)
    
    if request.method == 'PUT':
        tag.name = request.POST.get('name', '')
        tag.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Tag was successfully updated'
        }, status=404)
    elif request.method == 'DELETE':
        tag.delete()
        return JsonResponse({
            'status': 'success',
            'message': 'Tag was successfully deleted'
        }, status=404)
    else:
        return JsonResponse({'error': 'Access denied for this method: This method seems to be illegal in this world.'}, status=405)