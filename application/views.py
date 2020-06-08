from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from datetime import datetime
from django.utils import timezone

from users.models import AppUser

class LoginOrSignupAPI(APIView):

    '''
		Login, Create User 

		parameters:
			(Required)
			- token
			- name_id
			- username
			- bio
			- country
			- state
			- gender
			- age
			- image
			- nickname

	'''	
    def post(self, request):
    
    
        # get token from requested data 
        user_token = request.data.get('token', None)
        
        # check if there is requested token ...
        if user_token:

        	get_user = AppUser.objects.filter(user_token=user_token).first()
        	
        	# check if a user has this token ...
        	if get_user:
        		
        		# if the user has this token 
        		# update last login date
        		get_user.last_login_date = datetime.now()
        		# save data
        		get_user.save()
        		token = Token.objects.get_or_create(user=get_user)

        		# return data of the user
        		return Response({

        			'name_id': get_user.name_id,
        			'usenrame':get_user.username,
        			'bio': get_user.bio,
        			'reg': get_user.is_registered,
        			'certified': get_user.is_certified,
        			'image': get_user.image,
        			'token': token.key,       			
        			},
        			status=status.HTTP_200_OK)

        	# if token not exists in database ...
        	else:

        		# get requested name id 
        		name_id = request.data.get('name_id')
        		# check if name id exists ... ( because name id is unique)
        		if AppUser.objects.filter(name_id=name_id):

        			# if exists ...
        			# return bad reuqest
        			return Response({

        				'error': 'name_id is taken, please try another one!'
        				},
    				status=status.HTTP_400_BAD_REQUEST)

        		# if name id does not exist in the database ...
        		
        		# get requested data of the new user
        		username = request.data.get('username')
        		bio = request.data.get('bio')
        		email = request.data.get('email')
        		country = request.data.get('country')
        		city = request.data.get('city')
        		nickname = request.data.get('nickname')
        		visible_for_search = request.data.get('visible')
        		recieve_email = request.data.get('recieve_email')
        		gender = request.data.get('gender')
        		age = request.data.get('age')

        		image = request.FILES.get('image')
        		# create a new user (app user)
        		new_user = AppUser()

        		new_user.name_id = name_id
        		new_user.user_token = user_token
        		new_user.username = username
        		new_user.bio = bio
        		new_user.email = email
        		new_user.country = country
        		new_user.city = city
        		new_user.gender = gender
        		new_user.age = age
        		new_user.is_registered = True
        		new_user.image = image
        		new_user.nickname = nickname

        		new_user.register_date = datetime.now()
        		new_user.last_login_date = datetime.now()
        		
        		# save user in database after creating and updating fields 
        		new_user.save()

        		# generate token for the user 
        		token = Token.objects.get_or_create(user=new_user)
        		return Response({
        			'name_id' : new_user.name_id,
        			'username': new_user.username,
        			'bio': new_user.bio,
        			'reg': new_user.is_registered,
        			'certified': new_user.is_certified,
        			'image': new_user.image,
        			'token': token.key,
        			}, status=status.HTTP_201_CREATED)


        		# accounts (whatsapp , facebook, etc ...)
        		### Bool field 
        		# recieve mail from app (True, False)
        		# visible (True, False)

        # if there is no token ...
        # user will not be saved as registered user 
        # but the data of that user will be saved in our database
        else:

        	name_id = request.data.get('name_id')
        	username = request.data.get('username')
        	bio = request.data.get('bio')

        	new_user = AppUser()
        	
        	new_user.name_id = name_id
        	new_user.username = username
        	new_user.is_registered = False

        	new_user.save()

        	# generate token for user (not registered)
        	token = Token.objects.get_or_create(user=new_user)

        	return Response({
        			'username': new_user.username,
        			'name_id': new_user.name_id,
        			'bio': new_user.bio,
        			'reg': new_user.is_registered,
        			'certified': new_user.is_certified,
        			'image': new_user.image,
        			'token': token.key,
        			'token': token.key,
        		}, status=status.HTTP_201_CREATED)
