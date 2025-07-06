"""
Context Views Module
- Handles: Viewing and adding user context data
"""

import logging
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import Context
from ..serializers import ContextSerializer

# Setup logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ContextEntryListAPIView(generics.ListAPIView):
    """
    Returns a list of all context entries ordered by latest timestamp.
    """
    queryset = Context.objects.all().order_by("-timestamp")
    serializer_class = ContextSerializer


@api_view(["POST"])
def ContextEntryCreateAPIView(request):
    """
    Accepts POST request to create and save a new context entry.
    Logs success or failure messages.
    """
    serializer = ContextSerializer(data=request.data)
    if serializer.is_valid():
        context = serializer.save()
        logger.info("New context entry added: %s", context.content[:50])
        return Response(ContextSerializer(context).data, status=201)
    logger.warning("Invalid context data: %s", serializer.errors)
    return Response(serializer.errors, status=400)
