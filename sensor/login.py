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


def db_connect(): #database
    connection=psycopg2.connect(user = settings.DATABASE_USER1,password = settings.DATABASE_PASS1,host = settings.DATABASE_HOST1,port = "5432",database = settings.DATABASE_NAME1)
    return connection.cursor()


@csrf_exempt
def create_user(request):
    print("hello")
    username=request.GET.get('user')
    password = request.GET.get('password')
    user.objects.create(userid=username,password=password)

    return JsonResponse(('User created'),safe=False)


JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 3600

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
