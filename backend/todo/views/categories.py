"""
Category Views Module
- Handles: Listing of available categories
"""

from rest_framework import generics
from ..models import Category
from ..serializers import CategorySerializer


class CategoryListAPIView(generics.ListAPIView):
    """
    Returns a list of all available task categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
