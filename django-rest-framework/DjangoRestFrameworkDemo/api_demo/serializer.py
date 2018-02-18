from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):

    # note that a redefinition of the fields is not strictly necessary.
    # There are many other methods that we can add for steps like validation and so on

    # title = serializers.CharField(max_length=100)
    # description = serializers.CharField(max_length=200)
    # completed = serializers.BooleanField(default=True)


    class Meta:
        model = Task
        fields = ['title', 'description', 'completed'] # basically the fields that are required

