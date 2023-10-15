from django.http import JsonResponse

def get_element_or_404(Model, id):
    try:
        return Model.objects.get(id=id)
    except Model.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': f'Element with id {id} not found.'
        }, status=404)
