from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    usage_count = models.IntegerField(default=0)

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
    SOURCE_CHOICES = [('whatsapp', 'WhatsApp'), ('email', 'Email'), ('note', 'Note')]
    content = models.TextField()
    source_type = models.CharField(max_length=10, choices=SOURCE_CHOICES)
    processed_keywords = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

class Context(models.Model):
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    source_type = models.CharField(max_length=50, blank=True, null=True)

class Context(models.Model):
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    source_type = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.content[:50]