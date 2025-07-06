from django.db import models
from .constants.constants import (
    PRIORITY_CHOICES,
    STATUS_CHOICES,
    CATEGORY_CHOICES,
    CONTEXT_SOURCE_CHOICES
)


class Category(models.Model):
    """
    Represents a task category (e.g., Frontend, Backend).
    """
    name = models.CharField(max_length=100)
    usage_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Task(models.Model):
    """
    Represents a task in the to-do list.
    """
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="Medium")
    deadline = models.DateField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Pending")

    def __str__(self):
        return self.title


class ContextEntry(models.Model):
    """
    Stores contextual entries from sources like WhatsApp or Email.
    Used for AI keyword extraction and task generation.
    """
    content = models.TextField()
    source_type = models.CharField(max_length=10, choices=CONTEXT_SOURCE_CHOICES)
    processed_keywords = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.source_type.capitalize()}: {self.content[:40]}"


class Context(models.Model):
    """
    Stores general context data used for AI task suggestions.
    """
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    source_type = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.content[:50]
