from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from users.models import AdminUser # super admin,  admin, manager, supervisor
from .backends import authenticate

import uuid

class LoginAPI(APIView):
    '''
        Login API View
        Parameters are
            - email
            - password

        then authenticate by email and password
        if authenticate passes,
        it will return 200 code,
            name,
            email,
            role,
            phone,
            token
    '''
    def post(self,request):

        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)

        if not user:
            return Response({
                'error': 'Invalid Credentials'
            }, status=status.HTTP_400_BAD_REQUEST)

        token = Token.objects.create(user=user)

        return Response({
            'name':user.full_name,
            'email': user.email,
            'role': user.user_role,
            'phone': user.phone_number,
            'token': token.key
        },
        status=status.HTTP_200_OK)


class CreateUser(APIView):
    '''
    Create a new Dashboard User

    Parameters are:
        email
        phone
        name
        role (SA, A, M, S)
    '''
    def post(self,request):
        email = request.data.get('email')
        phone_number = request.data.get('phone')
        full_name = request.data.get('name')
        user_role = request.data.get('role')
        generated_password = request.data.get('password') #uuid.uuid4()

        # check if email exist
        if AdminUser.objects.filter(email=email).exists():
            return Response({
                'error': 'this email is already used.'
            }, status=status.HTTP_400_BAD_REQUEST)

        new_user = AdminUser()
        new_user.email = email
        new_user.phone_number = phone_number
        new_user.full_name = full_name
        new_user.user_role = user_role
        new_user.set_password(generated_password)
        new_user.save()

        return Response({}, status=status.HTTP_201_CREATED)

class LogoutAPI(APIView):
    '''
    Logout API View

    put Token in request Header

    Authorization : Token  <token>
    '''
    def post(self,request):
        if request.user and request.auth:
            request.user.auth_token.delete()
            request.user.save()
            return Response({},status=status.HTTP_200_OK)
        else:
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)
