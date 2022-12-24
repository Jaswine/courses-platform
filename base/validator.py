from django.core.exceptions import ValidationError

def img_size(value):
    filesize = value.size
    if filesize > 5000000:
            raise  ValidationError('Allowed size is 5 MB :]')