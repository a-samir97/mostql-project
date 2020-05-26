from users.models import AdminUser


def authenticate(email, password):
    # check if the email is exist ...
    if AdminUser.objects.filter(email=email).exists():
        # get the user by email
        user = AdminUser.objects.get(email=email)
        # check the password
        if user.check_password(password) is True:
            return user
    else:
        return None 
