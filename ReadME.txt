1. Create a virtual environment : python3 -m venv venv
2. Activate the virtual environment : source venv/bin/activate
3. install requirements.txt
4. create database storeline : restore database ( psql -U postgres -d storeline -f storelinedb.bak )
5. python3 manage.py runserver
6. migrate the changes.

settings file : deviceinfo/settings.py
source code : sensor/views.py

========= Database schema =======

device:
id = primary key
device_name = CharField
	
sensor:
id = primary key
sensor_type = CharField
device_id = ForeignKey('device')

sensor_data(models.Model):
data = CharField
data_time = DateTimeField
sensor_id = ForeignKey('sensor')

user(models.Model):
userid = CharField
password = CharField

--------------------------------

Used postman to test the APIs:

1. GET - http://127.0.0.1:8000/create_user/?user={username}&password={password}
2. POST- http://127.0.0.1:8000/login/
3. POST- http://127.0.0.1:8000/add_device/
          body - device:{device_name}   
4. POST- http://127.0.0.1:8000/update_device/?device_id={device_id}
5. POST- http://127.0.0.1:8000/sensor_data/
          body - device_id: {device_id}
                 sensor_type:{sensor_type}
                 sensor_data: {data}	          
6. GET - http://127.0.0.1:8000/get_sensor_data/?device_id={device_id}&start_time={start_time}&end_time={endtime}


   

