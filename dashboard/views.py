from django.db.models import Q
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from advertisement.models import *
from advertisement.serializers import PromocodeSerializer, AdsSerializer

from users.models import (
    AdminUser, # super admin,  admin, manager, supervisor,
    AppUser
)

from .models import Logging, Note, InboxMessages, CertifiedRequest, Reports

from .backends import authenticate
from .utils import serialize_data
from .serializers import (
    AppUserSerializer, 
    ShowBlockedUserSerializer,
    ShowInactiveUserSerializer,
    CertifiedRequestSerializer,
    ReportsSerializer,
    InboxMessagesSerializer
)

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

# get counts 
class MessagesCount(APIView):
    def get(self, request):
        reports_count = Reports.objects.all().count()
        messages_count = InboxMessages.objects.all().count()
        certified_count = CertifiedRequest.objects.all().count()

        return Response({
            'reports_count': reports_count,
            'messages_count': messages_count,
            'certified_count': certified_count
        }, status=status.HTTP_200_OK)

class UserCount(APIView):
    def get(self, request):
        
        males_count = AppUser.objects.filter(sex='M').count()
        females_count = AppUser.objects.filter(sex='F').count()
        registered_users_count = AppUser.objects.filter(is_registerd=True).count()
        unregistered_users_count = AppUser.objects.filter(is_registerd=False).count()
        all_users_count = AppUser.objects.all().count()

        return Response({
            'males_count': males_count,
            'females_count': females_count,
            'registered_count': registered_users_count,
            'unregistered_count': unregistered_users_count,
            'all_users_count': all_users_count
        }, status=status.HTTP_200_OK)

class AdminSystem(APIView):
    def get(self, request):
        all_logging = Logging.objects.all().count()
        all_ads_info = AdsInformation.objects.first()
        if all_ads_info:
            return Response({
                'all_logging': all_logging,
                'gps': all_ads_info.gps,
                'show_ads': all_ads_info.show_homepage and all_ads_info.show_settings and all_ads_info.show_profile,
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'there is no ads information, create a new one.'}, status=status.HTTP_400_BAD_REQUEST)

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

# Manage users
class ShowAppUser(APIView):
    def get(self, request):
        name_id =  request.data.get('name_id')
        get_user = AppUser.objects.filter(name_id=name_id).first()
        serializer = AppUserSerializer(get_user)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

class ShowBlockedUsers(APIView):
    def get(self, request):
        get_blocked_users = AppUser.objects.filter(is_blocked=True)
        serializer = ShowBlockedUserSerializer(get_blocked_users, many=True)
        return Response({'data':serializer.data}, status=status.HTTP_200_OK)

class ShowInactiveUsers(APIView):

    def get(self, request):
        # not registered users 
        all_not_registered_users = AppUser.objects.filter(is_registerd=False, is_certified=False)
        # registered users 
        all_registered_users = AppUser.objects.filter(is_registerd=True, is_certified=False)
        # certified users 
        all_certified_users = AppUser.objects.filter(is_registerd=True, is_certified=True)

        not_registered_users_list = []
        registered_users_list = []
        certified_users_list = []

        # looping for unregistered users 
        for user in all_not_registered_users:
            
            if user.last_login_date is None or user.last_view_date is None:
                continue

            if (timezone.now() - user.last_login_date).days >= 30 and \
                (timezone.now() - user.last_view_date).days >= 30:

                # append user to the unregistered user list
                not_registered_users_list.append(user)

        #looping for registered users 
        for user in all_registered_users:
            
            if user.last_login_date is None or user.last_view_date is None:
                continue

            if (timezone.now() - user.last_login_date).days >= 30 and \
                (timezone.now() - user.last_view_date).days >= 30:

                # append user to the registered users list 
                registered_users_list.append(user)
        
        # looping for certifed users 
        for user in all_certified_users:
            
            if user.last_login_date is None or user.last_view_date is None:
                continue

            if (timezone.now() - user.last_login_date).days >= 30 and \
                (timezone.now() - user.last_view_date).days >= 30:

                # append user to the certfied users list 
                certified_users_list.append(user)


        unregistered_users_serializer = ShowInactiveUserSerializer(not_registered_users_list, many=True)
        registered_users_serializer = ShowInactiveUserSerializer(registered_users_list, many=True)
        certified_users_serializer = ShowInactiveUserSerializer(certified_users_list, many=True)

        return Response({
            'unregistered_users': unregistered_users_serializer.data,
            'registered_users': registered_users_serializer.data,
            'certified_users': certified_users_serializer.data
        }, status=status.HTTP_200_OK)

class FilterAccount(APIView):
    def get(self, request):

        males_count = AppUser.objects.filter(sex='M').count()
        females_count = AppUser.objects.filter(sex='F').count()
        registered_count = AppUser.objects.filter(is_registerd=True, is_certified=False).count()
        certified_count = AppUser.objects.filter(is_registerd=True, is_certified=True).count()
        unregistered_count = AppUser.objects.filter(is_registerd=False, is_certified=False).count()
        all_users_count = AppUser.objects.all().count()
        range_13_to_21 = AppUser.objects.filter(Q(age__lte=21), Q(age__gte=13)).count()
        range_21_to_27 = AppUser.objects.filter(Q(age__lte=27), Q(age__gte=21)).count()
        range_27_to_35 = AppUser.objects.filter(Q(age__lte=35), Q(age__gte=27)).count()
        range_35_to_50 = AppUser.objects.filter(Q(age__lte=50), Q(age__gte=35)).count()
        above_50 = AppUser.objects.filter(Q(age__gt=50)).count()
        return Response({
            'males_count': males_count,
            'females_count': females_count,
            'registered_count': registered_count,
            'certified_count': certified_count,
            'unregistered_count': unregistered_count,
            'all_user_count': all_users_count,
            'range_13_21': range_13_to_21,
            'range_21_27': range_21_to_27,
            'range_27_25': range_27_to_35,
            'range_35_50': range_35_to_50,
            'above_50': above_50
        }, status=status.HTTP_200_OK)

# Application Management

class AdsInfo(APIView):
    '''
    for post method 
        gps : 
        show_all : true
        
        OR

        gps: 
        homepage: if true else don't send it 
        settings: if true else don't send it 
        profile: if true else don't send it 

    '''
    def get(self, request):
        info = AdsInformation.objects.first()
        if info:
            return Response({
                'gps': info.gps,
                'hompage':info.show_homepage,
                'settings': info.show_settings,
                'profile': info.show_profile
            }, status=status.HTTP_200_OK)

        return Response({
            'data': 'there is no information.'
        }, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        gps = request.data.get('gps')
        show_all = request.data.get('show_all')
        info = AdsInformation.objects.first()

        if info:
            if show_all:
                info.show_homepage = True
                info.show_settings = True
                info.show_profile = True
                info.gps = gps if gps else info.gps
                info.save()
                return Response({}, status=status.HTTP_200_OK)
            else:
                info.show_homepage = True if request.data.get('homepage') else False
                info.show_settings = True if request.data.get('settings') else False
                info.show_profile = True if request.data.get('profile') else False
                info.gps = gps if gps else info.gps
                info.save()
                return Response({}, status=status.HTTP_200_OK)
        else:
            if show_all:
                info = AdsInformation.objects.create(
                    gps=gps,
                    show_homepage=True,
                    show_settings=True,
                    show_profile=True
                )
                return Response({
                    'gps': info.gps,
                    'homepage': info.show_homepage,
                    'settings': info.show_settings,
                    'profile': info.show_profile 
                }, status=status.HTTP_201_CREATED)
            else:
                info = AdsInformation.objects.create(
                    gps=gps,
                    show_homepage=True if request.data.get('homepage') else False,
                    show_settings=True if request.data.get('settings') else False,
                    show_profile=True if request.data.get('profile') else False
                )
                return Response({
                    'gps': info.gps,
                    'homepage': info.show_homepage,
                    'settings': info.show_settings,
                    'profile': info.show_profile 
                }, status=status.HTTP_201_CREATED)

class DiscountValidation(APIView):
    '''
    For Post Method 

    '''
    def get(self, request):
        discount = Discount.objects.first()
        if discount:
            return Response({
                'manager_percentage': discount.manager_percentage,
                'manager_days':discount.manager_days,
                'supervisor_percentage':discount.supervisor_percentage,
                'supervisor_days':discount.supervisor_days
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'data': 'there is no discount validation, create a new one'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        discount = Discount.objects.first()
        if discount:
            discount.manager_percentage=request.data.get('manager_percentage') if request.data.get('manager_percentage') else discount.manager_percentage

            discount.manager_days=request.data.get('manager_days') if request.data.get('manager_days') else discount.manager_days
            
            discount.supervisor_percentage=request.data.get('supervisor_percentage') if request.data.get('supervisor_percentage') else discount.supervisor_percentage

            discount.supervisor_days=request.data.get('supervisor_days') if request.data.get('supervisor_days') else discount.supervisor_days

            discount.save()

            return Response({
                'manager_percentage': discount.manager_percentage,
                'manager_days':discount.manager_days,
                'supervisor_percentage':discount.supervisor_percentage,
                'supervisor_days':discount.supervisor_days    
            }, status=status.HTTP_200_OK)
        
        else:
            discount = Discount.objects.create(
                manager_percentage=request.data.get('manager_percentage'),
                manager_days=request.data.get('manager_days'),
                supervisor_percentage=request.data.get('supervisor_percentage'),
                supervisor_days=request.data.get('supervisor_days')
            )
            return Response({
                'manager_percentage': discount.manager_percentage,
                'manager_days':discount.manager_days,
                'supervisor_percentage':discount.supervisor_percentage,
                'supervisor_days':discount.supervisor_days
            }, status=status.HTTP_201_CREATED)

class AdsPrice(APIView):
    '''
    for post method 
        'days': number,
        'days_price': number,
        'appearing': number,
        'appearing_price': number
    '''
    def get(self, request):
        ads_pricing = AdvertisingPricing.objects.first()
        if ads_pricing:
            return Response({
                'days': ads_pricing.show_number_of_days,
                'days_price': ads_pricing.days_price,
                'appearing': ads_pricing.show_number_of_appearing,
                'appearing_price':ads_pricing.appearing_price   
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'data': 'there is not price plan, create a new one.'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        ads_pricing = AdvertisingPricing.objects.first()
        if ads_pricing:

            ads_pricing.show_number_of_days=request.data.get('days') if request.data.get('days') else ads_pricing.show_number_of_days 
            ads_pricing.days_price=request.data.get('days_price') if request.data.get('days_price') else ads_pricing.days_price 
            ads_pricing.show_number_of_appearing=request.data.get('appearing') if request.data.get('appearing') else ads_pricing.show_number_of_appearing
            ads_pricing.appearing_price=request.data.get('appearing_price') if request.data.get('appearing_price') else ads_pricing.appearing_price
            ads_pricing.save()

            return Response({
                'days': ads_pricing.show_number_of_days,
                'days_price': ads_pricing.days_price,
                'appearing': ads_pricing.show_number_of_appearing,
                'appearing_price':ads_pricing.appearing_price   
            }, status=status.HTTP_200_OK)

        else:
            ads_pricing = AdvertisingPricing.objects.create(
                show_number_of_days=request.data.get('days'),
                days_price=request.data.get('days_price'),
                show_number_of_appearing=request.data.get('appearing'),
                appearing_price=request.data.get('appearing_price')
            )
            return Response({
                'days': ads_pricing.show_number_of_days,
                'days_price': ads_pricing.days_price,
                'appearing': ads_pricing.show_number_of_appearing,
                'appearing_price':ads_pricing.appearing_price   
            }, status=status.HTTP_201_CREATED)

class InactiveInfo(APIView):
    '''
    for post method 
        'unreg_last_login':number,
        'unreg_last_view': number,
        'reg_last_login': number,
        'reg_last_view': number,
        'cer_last_login': number,
        'cer_last_view': number 
    '''
    def get(self, request):
        inactive_info = InactiveInformation.objects.first()
        if inactive_info:
            return Response({
                'unreg_last_login':inactive_info.unregistered_last_login,
                'unreg_last_view': inactive_info.unregistered_last_view,
                'reg_last_login': inactive_info.registered_last_login,
                'reg_last_view': inactive_info.registered_last_view,
                'cer_last_login':inactive_info.certified_last_login,
                'cer_last_view': inactive_info.certified_last_view
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'data': 'there is no inactive information, create a new one.'
            }, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        inactive_info = InactiveInformation.objects.first()
        if inactive_info:
            inactive_info.unregistered_last_login=request.data.get('unreg_last_login') if request.data.get('unreg_last_login') else inactive_info.unregistered_last_login 
            inactive_info.unregistered_last_view=request.data.get('unreg_last_view') if request.data.get('unreg_last_view') else inactive_info.unregistered_last_view 
            inactive_info.registered_last_login=request.data.get('reg_last_login') if request.data.get('reg_last_login') else inactive_info.registered_last_login  
            inactive_info.registered_last_view=request.data.get('reg_last_view') if request.data.get('reg_last_view') else inactive_info.registered_last_view
            inactive_info.certified_last_login=request.data.get('cer_last_login') if request.data.get('cer_last_login') else inactive_info.certified_last_login
            inactive_info.certified_last_view=request.data.get('cer_last_view') if request.data.get('cer_last_view') else inactive_info.certified_last_view

            inactive_info.save()
            return Response({
                'unreg_last_login':inactive_info.unregistered_last_login,
                'unreg_last_view': inactive_info.unregistered_last_view,
                'reg_last_login': inactive_info.registered_last_login,
                'reg_last_view': inactive_info.registered_last_view,
                'cer_last_login':inactive_info.certified_last_login,
                'cer_last_view': inactive_info.certified_last_view
            }, status=status.HTTP_200_OK)

        else:
            inactive_info = InactiveInformation.objects.create(
                unregistered_last_login=request.data.get('unreg_last_login'),
                unregistered_last_view=request.data.get('unreg_last_view'),
                registered_last_login=request.data.get('reg_last_login'),
                registered_last_view=request.data.get('reg_last_view'),
                certified_last_login=request.data.get('cer_last_login'),
                certified_last_view=request.data.get('cer_last_view')
            )
            return Response({
                'unreg_last_login':inactive_info.unregistered_last_login,
                'unreg_last_view': inactive_info.unregistered_last_view,
                'reg_last_login': inactive_info.registered_last_login,
                'reg_last_view': inactive_info.registered_last_view,
                'cer_last_login':inactive_info.certified_last_login,
                'cer_last_view': inactive_info.certified_last_view
            }, status=status.HTTP_201_CREATED)

class SendNotificationToAllUser(APIView):
    def post(self, request):
        pass


# Ads Managments

class PromoCode(APIView):
    def get(self, request):
        promo_codes = AdsPromocode.objects.all()
        serializer = PromocodeSerializer(promo_codes, many=True)
        return Response({'data':serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        user = AdminUser.objects.filter(id=request.user.id).first()
        if user:
            AdsPromocode.objects.create(
                user=user,
                code=request.data.get('code'),
                ratio=request.data.get('ratio'),
                valid_for=request.data.get('days'),
                reason=request.data.get('reason')
            )
            return Response({}, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'data': 'user is not authorized.'
            }, status=status.HTTP_401_UNAUTHORIZED)

class AdsRequests(APIView):
    def get(self, request):
        all_requested_ads = Advertising.objects.filter(accepted=False)
        serializer = AdsSerializer(all_requested_ads, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        pass

class ShowAds(APIView):
    def get(self, request):
        all_ads = Advertising.objects.filter(accepted=True)
        serializer = AdsSerializer(all_ads, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

## Messages Management 

class ReportsAPI(APIView):
    def get(self, request):
        all_reports = Reports.objects.all()
        serializer = ReportSerializer(all_reports, many=True)
        return Response({'data':serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        pass

class InboxMessagesAPI(APIView):
    def get(self, request):
        all_inbox = InboxMessages.objects.all()
        serializer = InboxMessagesSerializer(all_inbox, many=True)
        return Response({'data':serializer.data}, status=status.HTTP_200_OK)
    
    def post(self, request):
        pass

class CertifiedRequestAPI(APIView):
    def get(self, request):
        all_certified_request = CertifiedRequest.objects.all()
        serializer = CertifiedRequestSerializer(all_certified_request, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)
    
    def post(self, request):
        pass
