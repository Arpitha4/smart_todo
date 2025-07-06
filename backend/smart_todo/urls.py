from django.contrib import admin
from django.urls import path, include

# URL configuration for the Smart Todo project
urlpatterns = [
    path('admin/', admin.site.urls),              # Django admin panel
    path('api/', include('todo.urls')),           # API routes for scripts app
]
