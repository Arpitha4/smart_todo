"""
AI Task Generation View Module
- Handles: Creating new tasks from AI-based analysis of context
"""

import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers import TaskSerializer
from ..smart_ai import TaskAIProcessor

# Setup logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class AutoCreateTaskView(APIView):
    """
    Auto-creates a task from provided context using AI.
    Accepts POST request with context list.
    """

    def post(self, request):
        context_data = request.data.get("context", [])

        if not context_data:
            logger.warning("Context data not provided in request.")
            return Response({"error": "No context provided"}, status=400)

        try:
            # Flatten and extract context strings from dicts or strings
            extracted_context = []
            for item in context_data:
                if isinstance(item, dict) and "content" in item:
                    extracted_context.append(item["content"])
                elif isinstance(item, str):
                    extracted_context.append(item)

            # Call AI Processor to generate a new task
            ai_processor = TaskAIProcessor()
            ai_task = ai_processor.auto_create_task_from_context(extracted_context)

            # Save and return the generated task
            serializer = TaskSerializer(data=ai_task)
            if serializer.is_valid():
                task = serializer.save()
                logger.info("AI-generated task created: %s", task.title)
                return Response(TaskSerializer(task).data, status=201)

            # Handle validation errors
            logger.error("AI-generated task data is invalid: %s", serializer.errors)
            return Response(serializer.errors, status=400)

        except Exception as e:
            logger.exception("Error while auto-creating task from context: %s", e)
            return Response({"error": "Internal server error"}, status=500)
