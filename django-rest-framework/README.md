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
from django.urls import path
from django.contrib import admin
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include('api_demo.urls'))
]
```

urls.py of the app api
```python
from django.urls import path, re_path

from . import views

# Make sure that in the app urls file, you use views

urlpatterns = [
    path('tasks', views.task_list, name="task_list"),
    # these are basically the 2 types of api calls possible
    # 'task_list' is the name of the function in the view that is going to be called
    #  here note that we are using function based views and not class based views
    re_path('tasks/(?P<pk>[0-9]+)', views.task_detail, name="task_detail")
    # this regex actually tells us that after tasks there can be one number specifying the primary key of the task
    #  basically a unique number
]
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

from .models import Task
from .serializers import TaskSerializer # this is the serializer that we have written

@api_view(['GET', 'POST'])
def task_list(request):
	"""
	list all tasks or create new tasks
	"""
	if request.method == 'GET':
		tasks = Tasks.objects.all() # getting all objects
		serializer = TaskSerializer(tasks) # creating a serializer out of it
		return Response(serializers.data, many=True)

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

### Class Based Views

A class based view can actually reduce our code a lot more than a function based implementation. One of the key benefits of using class based views is that they allow us to compose bits of reusable behaviour. The generic views provided by REST framework allow us to quickly build API views that maps closely to your database models.

#### GenericAPIView

This class extends REST framework's APIView class, adding commonly required behaviour for standard list and detail views.

**Note:** Each of the concrete generic views is built by combining GenericAPIView, with one or more `mixins`.

#### Attributes:

**Basic Settings**

* `queryset`- The queryset that should be used for returning objects from this view. Typically you must either set this attribute or override the `get_queryset()` method. If you are overriding a view method it is important we call `get_queryset()` instead of directly accessing the `queryset` as `queryset` will get evaluated once and those results will remain cached for all subsequent requests.

* `serializer_class`- The serializer class that should be used for validating and deserializing the input and for serializing the output. Typically set this attribute or override the function `get_serializer_class()`.

* `lookup_field`- The model field that should be used for performing object lookup of individual model instances. Defaults to `pk`. Note when using the hyperlinked APIs you will need to ensure that both API views and the serializer classes set the lookup_field property if you need to use a custom value.

* `lookup_url_kwarg`- The url keyword argument that should be used for object lookup. The url conf should include a keyword argument corresponding to this value. If unset this defaults to using the same value as the 
`lookup_field`.

**Pagination:**

`pagination_class`- The pagination class that should be used when paginating list results. Defaults to the same value as the `DEFAULT_PAGINATION_CLASS` setting which is `rest_framework.pagination.PageNumberPagination`. Setting pagination class to None will actually remove pagination. 

**Filtering:**

`filter_backends`- A list of filter_backend classes that should be used for filtering the queryset. Defaults to the same value as the `DEFAULT_FITLER_BACKENDS` setting.

#### Methods:

* `get_queryset(self)`

Returns the queryset that should be used for list views, and that should be used for lookups in detail views. Defaults to returning the queryset specified by the `queryset` attribute.

Should be overriden to provide dynamic behavior:

```python
def get_queryset(self):
	user = self.request.user
	# so we can actually get the request object from the ListAPIView class objects for instance.
	return user.accouts.all()
```

* `get_object(self)`

Returns the object instane that should be used for detail view. Defaults to using the `lookup_field` parameter to filter the base queryset.

For providing more complex behavior should be overriden.

```python
def get_object(self):
	queryset = self.get_queryset()
	# we get the base queryset
	filter = {}
	for field in self.multiple_lookup_fields:
		filter[field] = self.kwargs[field]

	obj = get_object_or_404(queryset, **filters)
	self.check_object_permissions(self.request, obj)
	return obj


```

**Note:**
Few notes for the previous code:

When we write `**filters` it simply means we are passing the keys of the filter dictionary as keyword arguments to a function. So basically if we write 

```python
def fun(a=1, b=2):
	print(a)
	print(b)

fun()
```

This same code could also be written as 

```python
a = {'a':1, 'b':2}

def fun(**kwargs):
	for key in kwargs:
		print(kwargs[key])

fun(**a)
```
 Sometimes you will find functions written as:
 ```python
 def fun(*args, **kwargs):
 	pass
 ```

 Here basically `*args` is the positional arguments and **kwargs is the keyword arguments

 For more info have a look [here](https://www.saltycrane.com/blog/2008/01/how-to-use-args-and-kwargs-in-python/)

 Note that if your API does not have any object level permissions, you may optionally exclude the `self.check_object_permission` and simply return the object from get_object_or_404 lookup

* `filter_queryset(self, queryset)`

Given a queryset filter it with whichever filter backends are in use returning a new queryset

```python
def filter_queryset(self, queryset):
	filter_backends = (CategoryFilter, ) # that additional comma makes it a tuple actually

	if 'geo_route' in self.request.query_params:
		filter_backends = (GeoRouteFilter, CategoryFilter)
	elif 'geo_point' in self.request.query_params:
		filter_backends = (GeoPointFilter, CategoryFilter)

	for backend in list(filter_backends):
		queryset = backend().filter_queryset(self.request, queryset, view=self)

	return queryset
```

* `get_serializer_class(self)`

Returns the serializer class that should be used for the serializer. Defaults to returning the `serializer_class` attribute. 

```python
def get_serializer_class(self):
	if self.request.user.is_staff:
		return FullAccountSerializer
	return BasicAccountSerializer
```

#### Save and Deletion Hooks:

The following methods are provided by the mixin classes, and provide easy overriding of the object save and deletion behaviours

* `perform_create(self, serializer)`- Called by `CreateModelMixin` when saving a new object instance.
* `perform_update(self, serializer)`- Called by `UpdateModelMixin` when saving an existing object.
* `perform_destroy(self, instance)`- Called by `DestroyModelMixin` when deleting an object instance.

These hooks are particularly useful for setting attributes that are implicit in the request, but are not part of the request data. For instance, you might set an attribute on the object based on the request user, or based on a URL keyword argument.