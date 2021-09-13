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
# import pyjwt


def db_connect():
	connection=psycopg2.connect(user = settings.DATABASE_USER1,password = settings.DATABASE_PASS1,host = settings.DATABASE_HOST1,port = "5432",database = settings.DATABASE_NAME1)
	return connection.cursor()

def hello(requests):
	print("hello")

	return  HttpResponse(status=300)



@csrf_exempt
def add_device(request):   #call to check if device already exists with the name

	try:
		params = None
		data=request.POST

			
		device_obj = device.objects.filter(device_name=data['device'])
		if not device_obj:  
			device.objects.create(device_name=data['device']) # add device to device table

		
			device_obj = device.objects.filter(device_name=data['device'])
			sensor_obj = sensor.objects.filter(device_id=device_obj[0].id)

			#add sensor data to sensor table if not present already
			if not sensor_obj:
				sensor.objects.create(device_id=device_obj[0],sensor_type='Pressure')
				sensor.objects.create(device_id=device_obj[0],sensor_type='Temperature')

			print("success",device_obj[0])
			return JsonResponse(('Device, device id = '+str(device_obj[0].id) +' sensor type - 1. Temperature 2. Pressure  added successfully.'),safe=False)

		else:
			return JsonResponse(('Device exists with the same name, device id = '+str(device_obj[0].id)),safe=False)

	except:
		return JsonResponse(('Something went wrong'),safe=False)



@csrf_exempt
def update_device(request):   #if device exists update its name

	try:
		device_id=request.GET.get('device_id')
		data=request.POST
		device_obj = device.objects.filter(id=device_id)	

		if device_obj:  
			device.objects.filter(id=device_id).update(device_name=data['device']) #update device name
			return JsonResponse(('Device name updated from ' + str(device_obj[0].device_name) + ' to '+ data['device'] + ' , device id = '+str(device_obj[0].id)),safe=False)
		else:
			return JsonResponse(('No device to update'),safe=False)

	except:
		return JsonResponse(('Something went wrong'),safe=False)



@csrf_exempt
def add_sensor_data(request):    #if device exists add its continous data to sensor_data table

	try:
		date = datetime.now()
		data = request.POST
		device_obj = device.objects.filter(id=data['device_id'])

		if device_obj:    
			sensor_obj=sensor.objects.filter(device_id=device_obj[0],sensor_type=data['sensor_type'])
			sensor_data.objects.create(data_time=date,data=data['sensor_data'],sensor_id=sensor_obj[0])

			return  JsonResponse(('Data added successfully : device_name = ' + str(device_obj[0]) + ', sensor_type = '+str(data['sensor_type']) + ', data = '+str(data['sensor_data'])),safe=False)

		else:
			return  JsonResponse(('No device with device_id = ' + data['device_id']),safe=False)


	except:
		return JsonResponse(('Something went wrong'),safe=False)




@csrf_exempt
def get_sensor_data(request):   # query to get the device_name, sensor_type(pressure/temperature), sensor_data based on time and device_id imput

	try: 
		device_id = request.GET.get('device_id')
		start_time=request.GET.get('start_time')
		end_time=request.GET.get('end_time')

		
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

	except:
		return JsonResponse(('Something went wrong'),safe=False)

	
	



# >>> encoded_jwt = jwt.encode({"some": "payload"}, "secret", algorithm="HS256")
# >>> print(encoded_jwt)
# eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzb21lIjoicGF5bG9hZCJ9.Joh1R2dYzkRvDkqv3sygm5YyK8Gi4ShZqbhK2gxcs2U
# >>> jwt.decode(encoded_jwt, "secret", algorithms=["HS256"])
# {'some': 'payload'}