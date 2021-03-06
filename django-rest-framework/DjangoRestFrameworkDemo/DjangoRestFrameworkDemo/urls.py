"""
How django processes a request:
When a user requests a page from the Django powered site, this is the algorithm the system follows to determine which
python code to execute
1. Django determines the root URLconf module to use. This is set in the ROOT_URLCONF setting of settings.py, but if the
incoming HttpRequest object has a urlconf attribute (set by middleware), its value is used instead.
2. Django loads the python module and searches for urlpatterns variable. This should be a python list of django.urls.path

One important idea to note here is that urlpatterns must always be a list of path or re_path objects.

In the project url settings, make sure that path is  having an include to <app_name>.<url_module_name>
"""
from django.urls import path
from django.contrib import admin
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include('api_demo.urls'))
]