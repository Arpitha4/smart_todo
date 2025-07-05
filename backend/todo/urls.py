from django.urls import path
from .views import TaskListAPIView, CategoryListAPIView, ContextEntryListAPIView, TaskCreateAPIView, \
    AutoCreateTaskView, ContextEntryCreateAPIView, TaskUpdateAPIView

urlpatterns = [
    path('tasks/', TaskListAPIView.as_view()),
    path('tasks/<int:pk>/', TaskUpdateAPIView.as_view()),
    path('tasks/create/', TaskCreateAPIView.as_view()),
    path('tasks/auto-create/', AutoCreateTaskView.as_view()),
    path('categories/', CategoryListAPIView.as_view()),
    path('context/', ContextEntryListAPIView.as_view()),
    path('context/add/', ContextEntryCreateAPIView),
    path('tasks/auto-create/', AutoCreateTaskView.as_view()),
]
