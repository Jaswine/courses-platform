from django.shortcuts import render, redirect

from ..services import get_all_tags
from course.models import Tag


def tag_list_view(request):
    # all tags
    tags  = get_all_tags()
    
    if request.user.is_superuser:
        if request.method == 'POST':
            # get data from form
            tag = request.POST.get('tag')
            
            # create new tag
            tagForm = Tag.objects.create(name=tag)

            tagForm.save()
    else:
        return redirect('/')
    
        
    context = {
        'tags': tags.reverse(), 
        'user': request.user
    }
    return render(request,'base/tags.html', context)


def tag_delete_view(request, tag_id):
    if  request.user.is_superuser:
        # get tag
        tag = Tag.objects.get(id=tag_id)

        if tag:
            # delete tag
            tag.delete()
        else:
            messages.error(request, 'Tag not found')
        
        return redirect('/tags')
    else:
        return redirect('/')
