1. Create a virtual environment : python3 -m venv venv
2. Activate the virtual environment : source venv/bin/activate
3. install requirements.txt
4. create database storeline : restore database ( psql -U postgres -d storeline -f storelinedb.bak )
5. python3 manage.py runserver

Used postman to test the APIs:

	1. GET - http://127.0.0.1:8000/create_user/?user=storelineiot&password=iot

	2. POST - http://127.0.0.1:8000/login/

	3. POST - http://127.0.0.1:8000/add_device/
	   body - device:store
	   
	4. POST - http://127.0.0.1:8000/update_device/?device_id=1

	5. POST - http://127.0.0.1:8000/sensor_data/

	   body - device_id:1
	          sensor_type:Temperature
	          sensor_data:15
	          
	6. GET  - http://127.0.0.1:8000/get_sensor_data/?device_id=1&start_time=2021-09-11 00:08:30&end_time=2021-09-11 00:09:30


   

