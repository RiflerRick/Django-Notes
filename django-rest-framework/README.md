# Django Rest Framework

The django rest framework enables us to write api driven software. Essentially enabling us to create API endpoints for our application.

### Install django rest framework

```bash
pip install djangorestframework
```

### Create an api app

The api app is the place where we want to write all our code for the api.

### Update the settings file

The settings file must be updated with the currently created app and the rest_framework.
```python
INSTALLED_APPS = (
	"rest_framework",
	"api"
	)
``` 

### Create a new url as the api url

urls.py of the entire django project
```python
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
	'',
	url(r'^api/', include('api.urls')), # here is the api url we were talking about. 
	# Here we are simply including the api urls file
	url(r'^admin/', include(admin.site.urls))
	)

```

urls.py of the app api
```python
from django.conf.urls import patterns, url

urlpatterns = patterns(
	'api.views',
	url(r'^tasks/$', 'task_list', name='task_list'), # these are basically the 2 types of api calls possible
	# 'task_list' is the name of the function in the view that is going to be called
	# here note that we are using function based views and not class based views
	url(r'^tasks/(?P<pk>[0-9]+)$') 
	# this regex actually tells us that after tasks there can be one number specifying the primary key of the task
	# basically a unique number
	)
```

### Building a serializer

#### Serialization

Serialization in general is the process of translating data structures or object state into a format that can be stored for example in a file or memory buffer or transmitted across a network and reconstructed later. When the resulting series of the bits is reread according to the serialization format, it can be used to create a semantically identical clone of the original object. 

Here a serializer simply does that and here the objects are the models.

Lets say we have the following model

```python
from django.db import models

class Task(models.Model):
	completed = models.BooleanField(default=True)
	title = models.CharField(max_length=100)
	description = models.TextField()
```


We basically create a file `serializer.py` in the app api.

serializer.py
```python
from rest_framework import serializers

from task.models import Task # Task is the model here

class TaskSerializer(serializers.ModelSerializer):
	class Meta:
		model = Task
		fields = ('title', 'description', 'completed') # basically the fields
```

### Dealing with views

api/views.py
```python
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from task.models import Task
from api.serializers import TaskSerializer # this is the serializer that we have written

@api_view(['GET', 'POST'])
def task_list(request):
	"""
	list all tasks or create new tasks
	"""
	if request.method == 'GET':
		tasks = Tasks.objects.all() # getting all objects
		serializer = TaskSerializer(tasks) # creating a serializer out of it
		return Response(serializers.data)

	elif request.method == 'POST':
		serializer = TaskSerializer(data=request.DATA) # first creating a serializer with the data 
		if serializer.is_valid(): # if the validation is all okay then serializer is valid otherwise not
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)

		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'PUT', 'DELETE'])
def task_detail(request, pk): # recall that pk was used as part of the url itself
	"""
	Get, update or delete a specific task
	"""
	try:
		task = Task.objects.get(pk=pk)
	except Task.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == "GET":
		serializer = TaskSerializer(task) # gets data of a specific task
		return Response(serializer.data)

	elif request.method == "PUT":
		serializer = TaskSerializer(task, data=request.DATA)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
			
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	elif request.method == "DELETE":
		task.delete() # task mind you is a model object
		return Response(status=status.HTTP_204_NO_CONTENT)
```