from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Task
from .serializer import TaskSerializer

# This is an example of function based view for serializer

@api_view(['GET', 'POST'])
def task_list(request):
    """
    lists all tasks or creates a task
    :param request:
    :return:
    """
    if request.method == "GET":
        tasks = Task.objects.all()

        # tasks here is a query set. So we are essentially passing the entire query set into the serializer
        # the many=True attribute here is super important. Without this attribute an error would be raised

        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = TaskSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            # there is a validation error and hence there is a problem with the data in the request
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def task_detail(request, pk):
    """
    get update or delete a specific task
    :param request:
    :param pk:
    :return:
    """
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TaskSerializer(task, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            # returning the serializer data after saving it to the database
            return Response(serializer.data)

        else:
            # there were some validation errors with the data
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # recall we already have the task present
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)