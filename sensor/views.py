from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from sensor.models import *
from django.shortcuts import render, redirect
from rest_framework.response import Response
from django.conf import settings
import requests
from datetime import datetime, timedelta
import psycopg2
import json
import jwt



# jwt details
JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 3600

def db_connect(): #database
	connection=psycopg2.connect(user = settings.DATABASE_USER,password = settings.DATABASE_PASS,host = settings.DATABASE_HOST,port = "5432",database = settings.DATABASE_NAME)
	return connection.cursor()


#function to create user
@csrf_exempt
def create_user(request):
	print("hello")
	username=request.GET.get('user')
	password = request.GET.get('password')
	user.objects.create(userid=username,password=password)

	return JsonResponse(('User created'),safe=False)



# login function - creates auth token
@csrf_exempt
def login(request):

    post_data = request.POST

    print(post_data,"post_data")

    user1= user.objects.filter(userid=post_data['email'])
    if str(user1[0].password) == str(post_data['password']):
        payload = {
            'user_id': user1[0].userid,
            'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
        }

        jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
        print(jwt_token,"jwt_token")
        result = {'token':(jwt_token).decode('utf-8')}
        return JsonResponse((result),safe=False)

    else:
        return json_response({'message': 'Wrong credentials'}, status=400)


'''Call to add device-
request accepts device_name to add'''

@csrf_exempt
def add_device(request):   

	try:
		#read header and decode token
		jwt_token = request.META['HTTP_AUTHORIZATION']		
		auth = jwt_decode(jwt_token)
		if auth:
			data=request.POST
			device_obj = device.objects.filter(device_name=data['device'])
			if not device_obj:  
				device.objects.create(device_name=data['device']) # add device to device table
			
				device_obj = device.objects.filter(device_name=data['device'])
				sensor_obj = sensor.objects.filter(device_id=device_obj[0].id)

				if not sensor_obj:   #add sensor data to sensor table if not present already
					sensor.objects.create(device_id=device_obj[0],sensor_type='Pressure')
					sensor.objects.create(device_id=device_obj[0],sensor_type='Temperature')

				print("success",device_obj[0])
				return JsonResponse(('Device, device id = '+str(device_obj[0].id) +' sensor type - 1. Temperature 2. Pressure  added successfully.'),safe=False)
			else:
				return JsonResponse(('Device exists with the same name, device id = '+str(device_obj[0].id)),safe=False)
		else:
			return JsonResponse(('Autherization failed'),safe=False)
	except:
		return JsonResponse(('Autherization failed'),safe=False)


'''Call to update device name
request accepts device_name to update'''
@csrf_exempt
def update_device(request):   

	try:
		jwt_token = request.META['HTTP_AUTHORIZATION']		
		auth = jwt_decode(jwt_token)

		if auth:
			device_id=request.GET.get('device_id')
			data=request.POST
			device_obj = device.objects.filter(id=device_id)	

			if device_obj:  
				device.objects.filter(id=device_id).update(device_name=data['device']) #updates device name
				return JsonResponse(('Device name updated from ' + str(device_obj[0].device_name) + ' to '+ data['device'] + ' , device id = '+str(device_obj[0].id)),safe=False)
			else:
				return JsonResponse(('No device to update'),safe=False)
		else:
			return JsonResponse(('Autherization failed'),safe=False)
	except:
		return JsonResponse(('Autherization failed'),safe=False)


'''Call to add sensor data 
request accepts device_id,sensor_type,sensor_data to add'''
@csrf_exempt
def add_sensor_data(request):    

	try:
		jwt_token = request.META['HTTP_AUTHORIZATION']		
		auth = jwt_decode(jwt_token)

		if auth:
			date = datetime.now()
			data = request.POST
			device_obj = device.objects.filter(id=data['device_id'])

			if device_obj:    
				sensor_obj=sensor.objects.filter(device_id=device_obj[0],sensor_type=data['sensor_type'])
				sensor_data.objects.create(data_time=date,data=data['sensor_data'],sensor_id=sensor_obj[0])

				return  JsonResponse(('Data added successfully : device_name = ' + str(device_obj[0]) + ', sensor_type = '+str(data['sensor_type']) + ', data = '+str(data['sensor_data'])),safe=False)
			else:
				return  JsonResponse(('No device with device_id = ' + data['device_id']),safe=False)
		else:
			return JsonResponse(('Autherization failed'),safe=False)
	except:
		return JsonResponse(('Autherization failed'),safe=False)


'''Call to query the sensor data for a time period'''
@csrf_exempt
def get_sensor_data(request):  

	try:
		jwt_token = request.META['HTTP_AUTHORIZATION']		
		auth = jwt_decode(jwt_token)

		if auth:
			device_id = request.GET.get('device_id')
			start_time=request.GET.get('start_time')
			end_time=request.GET.get('end_time')

			#query to get sensor data
			select_query = '''SELECT sd.device_name,ss.sensor_type,ssd.data from 
			sensor_device sd inner join sensor_sensor ss on sd.id=ss.device_id_id
			inner join sensor_sensor_data ssd on ssd.sensor_id_id=ss.id where 
			ssd.data_time>='{}' and ssd.data_time<='{}' and sd.id={}	
			'''.format(start_time,end_time,device_id)

			print(select_query)
			cursor = db_connect()
			cursor.execute(select_query)

			query_result = [ dict(line) for line in [zip([ column[0] for column in cursor.description], row) for row in cursor.fetchall()] ]
			print(query_result) 
			if query_result:
				return JsonResponse((query_result),safe=False)
			else:
				return JsonResponse(('No data for the given inputs.'),safe=False)
		else:
			return JsonResponse(('Autherization failed'),safe=False)
	except:
		return JsonResponse(('Autherization failed'),safe=False)



# function for jwt token decode
def jwt_decode(token):

	token=token.split(' ')[1]
	print(token)
	decode=jwt.decode(token, JWT_SECRET, JWT_ALGORITHM)

	userid = decode['user_id']

	user_obj = user.objects.filter(userid=userid)
	print(user_obj,"user_obj")

	if user_obj.exists():
		return True
	else:
		return False

