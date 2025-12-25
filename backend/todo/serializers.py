from rest_framework import serializers
from .models import Task, Category, Context


# Serializer for Task model
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"  # Includes all fields from the Task model


# Serializer for Category model
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"  # Includes all fields from the Category model


# Serializer for Context model
class ContextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Context
        fields = ['id', 'content', 'timestamp', 'source_type']  # Specific fields to expose in API
