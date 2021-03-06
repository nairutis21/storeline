"""deviceinfo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from sensor.views import add_device,update_device,add_sensor_data,get_sensor_data,create_user,login
from django.views.generic import TemplateView
from django.conf.urls import url, include
import django


#api urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('create_user/',create_user),
    path('login/',login),
    path('add_device/',add_device),
    path('update_device/',update_device),
    path('sensor_data/',add_sensor_data),
    path('get_sensor_data/',get_sensor_data)
]
