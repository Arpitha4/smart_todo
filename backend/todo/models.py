from django.db import models


# Represents a task category (e.g., Frontend, Backend)
class Category(models.Model):
    name = models.CharField(max_length=100)  # Name of the category
    usage_count = models.IntegerField(default=0)  # Number of times the category has been used

    def __str__(self):
        return self.name


# Represents a task in the to-do list
class Task(models.Model):
    PRIORITY_CHOICES = [
        ("High", "High"),
        ("Medium", "Medium"),
        ("Low", "Low"),
    ]

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Started", "Started"),
        ("Completed", "Completed"),
    ]

    CATEGORY_CHOICES = [
        ("Frontend", "Frontend"),
        ("Backend", "Backend")
    ]

    title = models.CharField(max_length=255)  # Task title
    description = models.TextField(blank=True)  # Optional task description
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="Medium")  # Task priority
    deadline = models.DateField(null=True, blank=True)  # Optional deadline
    completed = models.BooleanField(default=False)  # Whether the task is completed
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)  # Task category
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Pending")  # Task status

    def __str__(self):
        return self.title


# Stores contextual entries from sources like WhatsApp or email
class ContextEntry(models.Model):
    SOURCE_CHOICES = [
        ('whatsapp', 'WhatsApp'),
        ('email', 'Email'),
        ('note', 'Note')
    ]

    content = models.TextField()  # Raw context content (message, note, etc.)
    source_type = models.CharField(max_length=10, choices=SOURCE_CHOICES)  # Source of the content
    processed_keywords = models.JSONField(default=list)  # Keywords extracted for AI processing
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of creation

    def __str__(self):
        return f"{self.source_type.capitalize()}: {self.content[:40]}"


# Stores general context used for AI task suggestions
class Context(models.Model):
    content = models.TextField()  # Raw content
    timestamp = models.DateTimeField(auto_now_add=True)  # When the context was added
    source_type = models.CharField(max_length=100, blank=True, null=True)  # Optional source info

    def __str__(self):
        return self.content[:50]
