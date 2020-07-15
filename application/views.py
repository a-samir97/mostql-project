from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from datetime import datetime
from django.utils import timezone
from django.core.files import File

from dashboard.models import CertifiedRequest, InboxMessages, Reports

from users.models import AppUser
from users.serializers import UserSerializer, UserShowSerializer, UnregisteredUserSerializer

from .models import UserStatus, Status, UserIP, LoginDates, VisitDates
from .utils import get_ip

import qrcode
from io import BytesIO

class ListAllUserAPI(APIView):
	'''
	to get all users in application 
	registered users and unregistered users 

	registered_users  : [],
	unregistered_users : []
	'''
	def get(self, request):
		registered_users = AppUser.objects.filter(is_registerd=True)
		unregistered_users = AppUser.objects.filter(is_registerd=False)

		registered_serializer = UserSerializer(registered_users, many=True)
		unregistered_serializer = UnregisteredUserSerializer(unregistered_users, many=True)
		return Response({
			'registered_users': registered_serializer.data,
			'unregistered_users': unregistered_serializer.data
		}, status=200)

class ListRegisteredUserAPI(APIView):
	'''
	To get registered users
	'''
	def get(self, request):
		all_registered_users = AppUser.objects.filter(is_registerd=True)
		serializer = UserSerializer(all_registered_users, many=True)
		return Response({'data': serializer.data}, status=200)

class ListNotRegisteredUserAPI(APIView):
	'''
	to get unregistered users 
	'''
	def get(self, request):
		all_unregistered_users = AppUser.objects.filter(is_registerd=False)
		serializer = UnregisteredUserSerializer(all_unregistered_users, many=True)
		return Response({'data': serializer.data}, status=200)

class ListCertifiedUsersAPI(APIView):
	def get(self, request):
		certified_users = AppUser.objects.filter(is_certified=True)
		serializer = UserSerializer(certified_users, many=True)
		return Response({'data': serializer.data}, status=200)

class ListNotCertifiedUsersAPI(APIView):
	def get(self, request):

		not_certified_users = AppUser.objects.filter(is_certified=False)
		serializer = UserSerializer(not_certified_users, many=True)
		return Response({'data': serializer.data}, status=200)

class RegisteredLoginAPI(APIView):
	'''
	For regitered users 
	Params: 
			{
            "user_token": "ad987sasqw89d4qwd", (unique and required)
            "login_via": "F", (F for facebook, G for google, N for None)
            "name_id": "tests", (unique and required)
            "username": "tests", 
            "bio": "bio",
            "email": "a.samirs971100@gmail.com", (unique but not required)
            "receive_email": true,
            "country": "Egypt",
            "state": "Cairo",
            "sex": "M",
            "age": 22,
            "nickname": "tessst", (used in search)
            "visible_in_search": true,
			"image: "your image"
            "accounts": {
                "phone": "jqwd",
                "phone_visible": false,
                "website": "qlkwdj",
                "website_visible": false,
                "whatsapp": "qlwkdqlwd",
                "whatsapp_visible": false,
                "facebook": "qlkwdhlqwhd",
                "facebook_visible": false,
                "instgram": "qlwkdhqlwihd",
                "instgram_visible": false,
                "gmail": "qlwkdhqlkwdh",
                "gmail_visible": false,
                "youtube": "qlkwjdqwjhd",
                "youtube_visible": true,
                "linkedin": "qlwjhdqlkwjd",
                "linkedin_visible": true,
                "twitter": "qo;kwqj;wdqw;d",
                "twitter_visible": true,
                "snapchat": "qlwhdqwidh",
                "snapchat_visible": false
            }
        }
	'''
	# this serializer for the registered user 
	serializer_class = UserSerializer
	parser_class = FileUploadParser

	def post(self, request):

		# if there is no token from google or facebook 
		if not request.data.get('user_token'):
			# return bad request 
			return Response({'error':'there is no token'}, status=status.HTTP_400_BAD_REQUEST)
		
		# check if the user has token
		if request.user and request.auth:
			# here user has logged in before 
			# so we will delete the token and generate a new one

			# get the current user 
			current_user = AppUser.objects.filter(id=request.user.id).first()
			# check if the current user is none 
			if not current_user:
				# return unauthroized user 
				return Response({}, status=status.HTTP_401_UNAUTHORIZED)
			
			# check if the requested user_token == current.user_token
			if request.data.get('user_token') != current_user.user_token:
				# return unauthorized response 
				return Response({}, status=status.HTTP_401_UNAUTHORIZED)

			# ip login today 
			current_user.ip_sign_in_today = get_ip(request)
		
			# last date for login 
			current_user.last_login_date = timezone.now()

			# save the object 
			current_user.save()

			# save ip of the user in the userIp model
			new_user_ip_object, _ = UserIP.objects.get_or_create(user=current_user, ip=current_user.ip_sign_in_today)

			# save login date of the user in logindates model 
			new_login_date_object, _ = LoginDates.objects.get_or_create(user=current_user, date=current_user.last_login_date)
			
			try:
				# delete the token of the current user 
				current_user.auth_token.delete()
			except:
				pass
			
			# generate a new token for the current user 
			token = Token.objects.create(user=current_user)
			
			# serialize current user data 
			serializer = UserShowSerializer(current_user)
			
			# return response 200 OK
			return Response({
				'data': serializer.data,
				'token': token.key
			}, status=status.HTTP_200_OK)

		# else, user has not any token 
		else:

			# serialize the requested data 
			serializer = UserSerializer(data=request.data)

			# check if the serializer is valid 
			if serializer.is_valid():
				
				# this is the first time 
				# save the data into our model
				new_user = serializer.save()
				
				# save the first ip
				new_user.first_ip = get_ip(request)

				# edit the last login date 
				new_user.last_login_date = timezone.now()

				# edit registered date 
				new_user.register_date = timezone.now()

				# is_registered to True
				new_user.is_registerd = True
				
				# save qrcode of the user 
				img = qrcode.make(new_user.name_id)
				blob = BytesIO()
				img.save(blob, 'JPEG')  
				
#				new_user.qr_code = img
				new_user.qr_code.save('{}_qrcode.jpg'.format(new_user.name_id), File(blob), save=False)
				
				# save after edit first ip
				new_user.save()

				# save ip of the user in the userIp model
				new_user_ip_object, _ = UserIP.objects.get_or_create(user=new_user, ip=new_user.first_ip)

				# save login date of the user in logindates model 
				new_login_date_object, _ = LoginDates.objects.get_or_create(user=new_user, date=new_user.last_login_date)

				# generate a new token 
				token = Token.objects.create(user=new_user)

				# show data serializer
				show_serializer = UserShowSerializer(new_user)

				# return Resonse Created
				return Response({

					'data': show_serializer.data, 
					'token': token.key 
				}, status=status.HTTP_201_CREATED)

class UnregisteredLoginAPI(APIView):
	'''
	For unregistered users
	Params:
	 {
            "name_id": "nanna", (unique and required)
            "username": "nanna", (required)
            "bio": "this is the first first bip",
            "email": "a.samir97@hotmail.com", (unique but not required)
            "receive_email": true,
            "country": "Egypt",
            "state": "Cairo",
            "sex": "M",
            "age": 22,
            "accounts": {
                "phone": "6645465798",
                "phone_visible": true,
                "website": "first website",
                "website_visible": false,
                "whatsapp": "",
                "whatsapp_visible": false,
                "facebook": "",
                "facebook_visible": false,
                "instgram": "",
                "instgram_visible": false,
                "gmail": "",
                "gmail_visible": false,
                "youtube": "",
                "youtube_visible": false,
                "linkedin": "",
                "linkedin_visible": false,
                "twitter": "",
                "twitter_visible": false,
                "snapchat": "",
                "snapchat_visible": false
            }
        }
	'''
	# this serializer for the unregistered user 
	serializer_class = UnregisteredUserSerializer
	parser_class = FileUploadParser

	def post(self, request):
		
		# check if the user has token ...
		if request.user and request.auth:
			
			# delete the token
			try:
				request.user.auth_token.delete()
			except:
				pass
			
			# get the current user 
			current_user = AppUser.objects.filter(id=request.user.id).first()

			# ip login today 
			current_user.ip_sign_in_today = get_ip(request)

			# last login date 
			current_user.last_login_date = timezone.now()

			# save the object 
			current_user.save()

			# generate a new token for the current user 
			token = Token.objects.create(user=current_user)

			# check if the user is not none 
			if not current_user:
				# return repsonse 
				return Response({}, status=status.HTTP_401_UNAUTHORIZED)

			# serialize data 
			serializer = UserShowSerializer(current_user)

			# return data and token 
			return Response({
				'data': serializer.data,
				'token': token.key
			})

		# else if user has not any token ...
		else:

			# get the requested data and serialize it 
			serializer = UnregisteredUserSerializer(data=request.data)

			# check if the serializer is valid 
			if serializer.is_valid():
				
				# first time to login 
				
				# save the serializer 
				new_user = serializer.save()

				# save the first ip
				new_user.first_ip = get_ip(request)

				# last login date
				new_user.last_login_date = timezone.now()

				# register date 
				new_user.register_date = timezone.now()

				# save new user model after editing 
				new_user.save()

				# generate a new token 
				token = Token.objects.create(user=new_user)

				# show serializer 
				show_serialzier = UserShowSerializer(new_user)

				# return data and token 
				return Response({
					'data': show_serialzier.data,
					'token': token.key
				}, status=status.HTTP_201_CREATED)

			# if serializer is not valid 
			else:
				return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class ViewAccountAPI(APIView):

	def get(self, request, name_id):

		get_viewed_user = AppUser.objects.filter(name_id=name_id).first()
		
		if get_viewed_user:
			get_viewed_user.last_view_date = timezone.now()
			
			# save last visit dates 
			last_visit_date_object, _ = VisitDates.objects.get_or_create(user=get_viewed_user, date=timezone.now())

			get_viewed_user.save()
			return Response({}, status=status.HTTP_200_OK)
		else:
			return Response({'error': 'user is not found.'}, status=status.HTTP_404_NOT_FOUND)

class SearchByNameID(APIView):
	def get(self, request):
		'''get users by name_id
		Params:
			{
				q : ""
			}	
		'''
		searched_data = request.data.get('q')
		if searched_data:
			users = AppUser.objects.filter(name_id__icontains=searched_data)
			serializer = UserShowSerializer(users, many=True)
			return Response({
				'data': serializer.data
			}, status=status.HTTP_200_OK)
		else:
			return Response({}, status=status.HTTP_400_BAD_REQUEST)

class SearchByUsername(APIView):
	'''
	to get users by username
	Params:
	{
		q : ""
	}	
	'''
	def get(self, request):
		searhed_data = request.data.get('q')
		if searhed_data:
			users = AppUser.objects.filter(username__icontains=searhed_data)
			serializer = UserShowSerializer(users, many=True)
			return Response({
				'data': serializer.data
			}, status=status.HTTP_200_OK)
		else:
			return Response({}, status=status.HTTP_400_BAD_REQUEST)

class SearchByNickname(APIView):
	'''
	to get users by nickname
	Params:
		{
			q : ""
		}	
	'''
	def get(self, request):	
		searched_data = request.data.get('q')
		if searched_data:
			users = AppUser.objects.filter(nickname__icontains=searched_data)
			serializer = UserShowSerializer(users, many=True)
			return Response({
				'data': serializer.data
			}, status=status.HTTP_200_OK)
		else:
			return Response({}, status=status.HTTP_400_BAD_REQUEST)

class SearchByBio(APIView):
	'''
	search for users by bio 
	Params:
		{
			q: " "
		}
	'''
	def get(self, request):
		searched_data = request.data.get('q')
		if searched_data:
			users = AppUser.objects.filter(bio__icontains=searched_data)
			serializer = UserShowSerializer(users, many=True)
			return Response({
				'data': serializer.data
			}, status=status.HTTP_200_OK)
		else:
			return Response({}, status=status.HTTP_400_BAD_REQUEST)

class ToggleFollowingAPI(APIView):
	def post(self, request, name_id):
		
		# get the current user 
		current_user = AppUser.objects.filter(id=request.user.id).first()

		# get the selected user that we want to toggle follow 
		user = AppUser.objects.filter(name_id=name_id).first()

		# check if the user exists in the database
		if user:
			# check if that user is in following list 
			if user in current_user.friends_list.all():
				
				# unfollow user here 
				current_user.friends_list.remove(user)
				
				# return OK response 
				return Response({}, status=status.HTTP_200_OK)

			# else if user does not exist in the following list 
			else:
				# follow user 
				current_user.friends_list.add(user)

				# get user status to createa a new status 
				user_status_object, _ = UserStatus.objects.get_or_create(user=user)
				
				# create a new status that hold follow action
				status_user = Status.objects.create(action='{} follow you'.format(current_user.name_id))
				
				# add the new status to the user status list
				user_status_object.status.add(status_user)

				# return OK response 
				return Response({}, status=status.HTTP_200_OK)

		# if user does not exist in the database
		else:
			return Response({}, status=status.HTTP_404_NOT_FOUND)

class AddUserAPI(APIView):
	
	def post(self, request, name_id):
		
		# get the current user 
		current_user = AppUser.objects.filter(id=request.user.id).first()
		# if user does not exist 
		if not current_user:
			# return not found response
			return Response({}, status=status.HTTP_404_NOT_FOUND)
		
		# get the user that the current user want to add 
		user = AppUser.objects.filter(name_id=name_id).first()

		# check if user does not exist in the database ...
		if not user:
			# return not found reponse 
			return Response({}, status=status.HTTP_404_NOT_FOUND)
		
		# if the current user and the selected user exist ...

		# we want to make sure that the current user is not exist in the friends list of the user
		if current_user in user.friends_list.all():
			# return bad request 
			# i think it will not happen but to make sure 
			return Response({}, status=status.HTTP_400_BAD_REQUEST)
		
		# we want to make sure that the current user is not exist in the status list (watiting list)
		# if the current user in the waiting list, so the current user can not send add 

		if current_user in user.status_list.all():
			# return bad request 
			# the user is already in the status list
			return Response({}, status=status.HTTP_400_BAD_REQUEST)
		
		# after all checks 
		# we can add current user into status list of the user
		# status_list like waiting list  
		user.status_list.add(current_user)

		return Response({}, status=status.HTTP_201_CREATED)

class ConfirmAddAPI(APIView):

	def post(self, request):
		# get the current user 
		current_user = AppUser.objects.filter(id=request.user.id).first()
	
		# if the current user is none 
		if not current_user:
			# return response  
			return Response({}, status=status.HTTP_401_UNAUTHORIZED)

		# get the user from the requested data 
		name_id = request.data.get('name_id')

		# if name_id is none 
		if not name_id:
			# return bad request 
			return Response({}, status=status.HTTP_400_BAD_REQUEST)
		
		# get user by name_id 
		user = AppUser.objects.filter(name_id=name_id).first()

		# check if the user in the status list of the current user
		if user in current_user.status_list.all():
			# remove the user from the status list
			current_user.status_list.remove(user)
			# add user to the friend list of current user
			current_user.friends_list.add(user)
			# add current user to the friend list of user 
			user.friends_list.add(current_user)

			# create status for the two users 
			
			# get or create user status object for the current user
			current_user_status_object, _ = UserStatus.objects.get_or_create(user=current_user)
			# get or create user status object for the user 
			user_status_object, _ = UserStatus.objects.get_or_create(user=user)
			# create a new status object for the current user 
			current_user_status = Status.objects.create(action='you and {} are now friends'.format(user.name_id))
			# create a new status object for the user 
			user_status = Status.objects.create(action='you and {} are now friends'.format(current_user.name_id))
			# put the new status for current user to the status list 
			current_user_status_object.status.add(current_user_status)
			# put the new statis for the user to the status list 
			user_status_object.status.add(user_status)

			# return OK response 
			return Response({}, status=status.HTTP_200_OK)

		# if the user is not exist in the status list
		else:
			# return bad request
			# i think it will not happen but to make sure
			return Response({}, status=status.HTTP_400_BAD_REQUEST)

class RejectUserAPI(APIView):

	def post(self, request):
		
		# get the current user
		current_user = AppUser.objects.filter(id=request.user.id).first()

		# if the current user is none
		if not current_user:
			# return response 401 
			return Response({}, status=status.HTTP_401_UNAUTHORIZED)

		# get the name id of the requested data 
		name_id = request.data.get('name_id')

		# check if the name id is none 
		if not name_id:
			# return response 400 bad request
			return Response({}, status=status.HTTP_400_BAD_REQUEST)
		
		# get the user by name_id
		user = AppUser.objects.filter(name_id=name_id).first()

		# if the user is none 
		if not user:
			# return response bad request
			return Response({}, status=status.HTTP_400_BAD_REQUEST)

		# if the user is in the status list of the current user 
		if user in current_user.status_list.all():
			# remove user from the status_list 
			current_user.status_list.remove(user)

			# create a new status for the rejection
			user_status_object, _ = UserStatus.objects.get_or_create(user=user)
			# create new status with rejection action 
			status_object = Status.objects.create(action='{} reject you'.format(current_user.name_id))
			# add status to user status list 
			user_status_object.status.add(status_object)

			# return respons ok 
			return Response({}, status=status.HTTP_200_OK)

class GetFriendsListAPI(APIView):
	
	def get(self, request):
		# get the current user
		current_user = AppUser.objects.filter(id=request.user.id).first()

		# if current user is none 
		if not current_user:
			# return anuthorized response 
			return Response({}, status=status.HTTP_401_UNAUTHORIZED)
		
		# get all friends of current user 
		all_friends = current_user.friends_list.all()

		# serialize data (convert to JSON)
		serializer = UserShowSerializer(all_friends)
		# return OK Response 
		return Response({'data': serializer.data}, status=status.HTTP_200_OK)

class GetWaitingListAPI(APIView):
	
	def get(self, request):
		# get the current user 
		current_user = AppUser.objects.filter(id=request.user.id).first()

		# check if the current user is none 
		if not current_user:
			# return unauthorized user 
			return Response({}, status=status.HTTP_401_UNAUTHORIZED)
		
		# get all waiting list of the current user 
		waiting_list = current_user.status_list.all()

		# serialize data 
		serializer = UserShowSerializer(waiting_list)

		# return Ok Response 
		return Response({'data': serializer.data}, status=status.HTTP_200_OK)

class CertifiedRequestAPI(APIView):
	def post(self, request):
		user = AppUser.objects.filter(id=request.user.id).first()
		if user:
			certified_request = CertifiedRequest.objects.filter(user=user).first()
			if certified_request:
				# user has asked for certification before 
				return Response(
					{'data': 'you have asked for certification before'}, 
				status=status.HTTP_400_BAD_REQUEST)
			else:
				certified_request = CertifiedRequest.objects.create(
					user=user,
					reason=request.data.get('reason'),
					proof=request.data.get('proof'),
				)
				return Response({
					'username': user.name_id,
					'reason': certified_request.reason,
					'proof': certified_request.proof
				}, status=status.HTTP_201_CREATED)
		else:
			return Response({}, status=status.HTTP_401_UNAUTHORIZED)

class CreateReport(APIView):
	def post(self, request):
		user = AppUser.objects.filter(id=request.user.id).first()
		if user:
			# creating report 
			new_report = Reports.objects.create(
				user=user,
				report_reason=request.data.get('reason'),
				notes=request.data.get('notes')
			) 
			return Response({
				'name_id': user.name_id,
				'reason': new_report.report_reason,
				'notes': new_report.notes
			}, status=status.HTTP_201_CREATED)
			
		else:
			return Response({}, status=status.HTTP_401_UNAUTHORIZED)

class CreateMessage(APIView):
	def post(self, request):
		user = AppUser.objects.filter(id=request.user.id).first()
		if user:
			# create a new message 
			new_message = InboxMessages.objects.create(
				user=user,
				message=request.data.get('message'),
			)
			return Response({
				'name_id': user.name_id,
				'message': new_message.message
			}, status=status.HTTP_201_CREATED)
		else:
			return Response({}, status=status.HTTP_401_UNAUTHORIZED)