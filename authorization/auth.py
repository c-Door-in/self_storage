from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        print(UserModel)
        try:
            user = UserModel.objects.get(email=username)
            print(user)
        except UserModel.DoesNotExist:
            print('doent exist')
            return None
        else:
            if user.check_password(password):
                print(True)
                return user
        print(False)
        return None
