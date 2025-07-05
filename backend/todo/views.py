# views.py

from rest_framework import generics, status, serializers
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Task, Category, Context
from .serializers import TaskSerializer, CategorySerializer, ContextSerializer
from .smart_ai import auto_create_task_from_context


# ---------- Task APIs ----------

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


# ---------- Category API ----------

class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# ---------- Context APIs ----------

# List all context entries
class ContextEntryListAPIView(generics.ListAPIView):
    queryset = Context.objects.all().order_by("-timestamp")
    serializer_class = ContextSerializer


# Add a new context entry
@api_view(["POST"])
def ContextEntryCreateAPIView(request):
    serializer = ContextSerializer(data=request.data)
    if serializer.is_valid():
        context = serializer.save()
        return Response(ContextSerializer(context).data, status=201)
    return Response(serializer.errors, status=400)


# ---------- AI Task Auto-Creation API ----------

class AutoCreateTaskView(APIView):
    def post(self, request):
        context_data = request.data.get("context", [])
        if not context_data:
            return Response({"error": "No context provided"}, status=400)

        ai_task = auto_create_task_from_context(context_data)
        serializer = TaskSerializer(data=ai_task)
        if serializer.is_valid():
            task = serializer.save()
            return Response(TaskSerializer(task).data, status=201)

        return Response(serializer.errors, status=400)
