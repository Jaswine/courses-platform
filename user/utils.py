from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User

# user authentication for sign in
def authenticate(email, password):
   try:
      user = User.objects.get(email=email)
      
      if check_password(password, user.password):
         return user
      return None
   except:
      return None