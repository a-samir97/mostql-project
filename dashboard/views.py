from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from users.models import AdminUser # super admin,  admin, manager, supervisor
from .models import Logging, Note

from .backends import authenticate
from .utils import serialize_data

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

        # save action
        if user.user_role != "SA":
            Logging.objects.create(
                user=user,
                action="login",
                )

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

            admin_user = AdminUser.objects.filter(email=request.user.email).first()

            if admin_user:
		    # save action
                if admin_user.user_role != "SA":
                  Logging.objects.create(
                  user=admin_user,
                  action="logout"
                  )
            return Response({},status=status.HTTP_200_OK)

        else:
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)

class LoggingAPI(APIView):

    def get(self, request):
        if request.user and request.auth:
            admin_user = AdminUser.objects.filter(email=request.user.email).first()
            if admin_user:

                # if the user is super admin ...

                if admin_user.user_role == "SA":

                    # will return all logging data
                    # admins, managers, supervisors

                    admins_logging = serialize_data(Logging.objects.filter(user__user_role='A'))
                    managers_logging = serialize_data(Logging.objects.filter(user__user_role='M'))
                    supervisors_logging = serialize_data(Logging.objects.filter(user__user_role='S'))

                    return Response({
                        'admins': admins_logging,
                        'managers': managers_logging,
                        'supervisors': supervisors_logging,
                        },
                        status=status.HTTP_200_OK)

                # if the user is admin ...

                elif admin_user.user_role == "A":

                    # will return data of admins, managers and supervisors only
                    admins_logging = serialize_data(Logging.objects.filter(user__user_role='A'))      
                    managers_logging = serialize_data(Logging.objects.filter(user__user_role='M'))
                    supervisors_logging = serialize_data(Logging.objects.filter(user__user_role='S'))

                    return Response({
                        'admins': admins_logging,
                        'managers': managers_logging,
                        'supervisors': supervisors_logging,
                        },
                        status=status.HTTP_200_OK)

                # if the user is manager ...

                elif admin_user.user_role == "M":

                    # will reutrn data of managers, supervisors only
                    managers_logging = serialize_data(Logging.objects.filter(user__user_role='M'))
                    supervisors_logging = serialize_data(Logging.objects.filter(user__user_role='S'))

                    return Response({
                        'managers': managers_logging,
                        'supervisors': supervisors_logging,
                        },
                        status=status.HTTP_200_OK)

                # if the user is supervisor ...

                elif admin_user.user_role == 'S':

                    # can not see any logging..
                    return Response({}, status=status.HTTP_200_OK)

                # if user role is not exist ...
                # i think it will not happen ...
                # but let's handle this ...

                else:
                    return Response({}, status=status.HTTP_400_BAD_REQUEST)

        # if user is not authenticated
        else:
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)

class NoteAPI(APIView):
    
    def get(self, request):

        all_notes = Note.objects.all()
        result = []
        for note in all_notes:
            result.append({
                'id':note.id,
                'title': note.title,
                'description': note.description,
                'date': note.date,
                'url': note.url
            })
        
        return Response({
            'data': result
        }, status=status.HTTP_200_OK)
    
    def post(self, request):
        '''
        parameters :
            - title (required)
            - description (required)
            - date (required)
            - url (not required)
        '''
        title = request.data.get('title')
        description = request.data.get('description')
        date = request.data.get('date')
        url = request.data.get('url')

        if title is None or description is None \
            or date is None:

            return Response({
                'error': 'please fill all inputs.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        new_note = Note()
        new_note.title = title
        new_note.description = description
        new_note.date = date
        new_note.url = url
        new_note.save()

        return Response({}, status=status.HTTP_201_CREATED)

class DeleteNote(APIView):

    def delete(self, request, id):
        
        deleted_note = Note.objects.filter(id=id).first()

        if deleted_note:
            deleted_note.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        else:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

# list all users except (super admin)
class ListUserAPI(APIView):
    
    def get(self, request):
        '''
        get all admin users except super admin

        '''
        all_users = AdminUser.objects.all().exclude(Q(user_role='SA'))

        json_data = []

        for user in all_users:
            json_data.append({
                'id': user.id,
                'role': user.user_role,
                'phone': user.phone_number,
                'name': user.full_name,
                'email': user.email,
                'blocked': user.is_blocked,
                })

        return Response({'users': json_data}, status=status.HTTP_200_OK)

class DeleteUserAPI(APIView):

    def delete(self, request, user_id):
        '''
        delete user by phone
        '''
        get_user = AdminUser.objects.filter(id=user_id).first()

        if get_user:

            get_user.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        else:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

class ToggleBlockUserAPI(APIView):
    def post (self, request, user_id):
        get_user = AdminUser.objects.filter(id=user_id).first()

        if get_user:
            get_user.is_blocked = True if get_user.is_blocked == False else False
            get_user.save()

            return Response({"blocked": get_user.is_blocked}, status=status.HTTP_201_CREATED)
        else:
            return Response({}, status=status.HTTP_404_NOT_FOUND)