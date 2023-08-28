
# Password checking
def password_checking(user, password, password_confirmation):
   if password == password_confirmation:
      if password != user.password:
         if len(password) < 8:
            return [True, 'OK']
         else:
            return [False, 'password is too short']
      else:
         return [False, 'password == user.password']
   else:
      return [False, 'confirm password is not the same']