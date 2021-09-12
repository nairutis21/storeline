from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import JSONField

# Create your models here.



class device(models.Model):
	device_name = models.CharField(max_length=60,null=True, blank=True)

	def __str__(self):
		return self.device_name

class sensor(models.Model):
	sensor_type = models.CharField(max_length=10,null=True, blank=True)
	device_id = models.ForeignKey('device',on_delete=models.CASCADE,null=True, blank=True)

	def __str__(self):
		return self.device_id
	

class sensor_data(models.Model):
	data = models.CharField(max_length=100,null=True, blank=True)
	data_time = models.DateTimeField(blank=True, null=True)
	sensor_id = models.ForeignKey('sensor',on_delete=models.CASCADE,null=True, blank=True)

	def __str__(self):
		return self.sensor_id