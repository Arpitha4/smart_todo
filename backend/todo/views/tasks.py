from rest_framework import generics
from ..models import Task
from ..serializers import TaskSerializer


class TaskListAPIView(generics.ListAPIView):
    queryset = Task.objects.all().order_by('-priority', 'deadline')
    serializer_class = TaskSerializer


class TaskCreateAPIView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'pk'
