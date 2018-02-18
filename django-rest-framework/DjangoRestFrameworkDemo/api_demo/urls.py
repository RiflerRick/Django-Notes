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