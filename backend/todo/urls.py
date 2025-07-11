from django.urls import path
from .views.tasks import TaskListAPIView, TaskCreateAPIView, TaskUpdateAPIView
from .views.context import ContextEntryListAPIView, ContextEntryCreateAPIView
from .views.ai import AutoCreateTaskView
from .views.categories import CategoryListAPIView

urlpatterns = [
    path('tasks/', TaskListAPIView.as_view()),                      # Get list of all tasks
    path('tasks/<int:pk>/', TaskUpdateAPIView.as_view()),          # Update a task by its ID
    path('tasks/create/', TaskCreateAPIView.as_view()),            # Create a new task manually
    path('tasks/auto-create/', AutoCreateTaskView.as_view()),      # Auto-create a task from context using AI
    path('categories/', CategoryListAPIView.as_view()),            # Get list of all categories
    path('context/', ContextEntryListAPIView.as_view()),           # Get list of all context entries
    path('context/add/', ContextEntryCreateAPIView),               # Add a new context entry
]
