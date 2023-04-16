from django.contrib import messages


def len_checking(field, number):
   if (len(field) == number):
      return True
   else:
      messages.error('{} must be at least {} characters'.formats(field, number))
      return False

def slug_checking(objects, slug):
   for course in objects:
      if slug == course.slug:
         messages.error(request, 'This article already exists')
         return False

def isNotNone(field):
   if (field == None ):
      messages.error(request, 'Tag must be selected')  
      return False 