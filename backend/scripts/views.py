import logging
from rest_framework import generics, status, serializers
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Task, Category, Context
from .serializers import TaskSerializer, CategorySerializer, ContextSerializer
from .smart_ai import TaskAIProcessor

# Configure module-level logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# ---------- Task APIs ----------

class TaskListAPIView(generics.ListAPIView):
    """
    API view to list all tasks, ordered by priority and deadline.
    """
    queryset = Task.objects.all().order_by('-priority', 'deadline')
    serializer_class = TaskSerializer


class TaskCreateAPIView(generics.CreateAPIView):
    """
    API view to manually create a new task.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    API view to retrieve and update a task using its primary key.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'pk'


# ---------- Category API ----------

class CategoryListAPIView(generics.ListAPIView):
    """
    API view to list all available task categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# ---------- Context APIs ----------

class ContextEntryListAPIView(generics.ListAPIView):
    """
    API view to list all context entries ordered by timestamp.
    """
    queryset = Context.objects.all().order_by("-timestamp")
    serializer_class = ContextSerializer


@api_view(["POST"])
def ContextEntryCreateAPIView(request):
    """
    Function-based API view to create a new context entry.
    """
    serializer = ContextSerializer(data=request.data)
    if serializer.is_valid():
        context = serializer.save()
        logger.info("New context entry added: %s", context.content[:50])
        return Response(ContextSerializer(context).data, status=201)
    logger.warning("Invalid context data: %s", serializer.errors)
    return Response(serializer.errors, status=400)


# ---------- AI Task Auto-Creation API ----------

class AutoCreateTaskView(APIView):
    """
    API view to auto-create a task using AI based on provided context data.
    """

    def post(self, request):
        context_data = request.data.get("context", [])

        if not context_data:
            logger.warning("Context data not provided in request.")
            return Response({"error": "No context provided"}, status=400)

        try:
            auto_create_task_from_context = TaskAIProcessor.auto_create_task_from_context
            ai_task = auto_create_task_from_context(context_data)
            serializer = TaskSerializer(data=ai_task)

            if serializer.is_valid():
                task = serializer.save()
                logger.info("AI-generated task created: %s", task.title)
                return Response(TaskSerializer(task).data, status=201)

            logger.error("AI-generated task data is invalid: %s", serializer.errors)
            return Response(serializer.errors, status=400)

        except Exception as e:
            logger.exception("Error while auto-creating task from context: %s", e)
            return Response({"error": "Internal server error"}, status=500)
