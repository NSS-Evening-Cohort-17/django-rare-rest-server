"""View module for handling requests about categories"""
from os import defpath
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.core.exceptions import ValidationError
from rareapi.models import Category

class CategoryView(ViewSet):
    """Rare categories view"""
    
    def retrieve(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category)
            return Response(serializer.data)
        except Category.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
    def list(self, request):
        """Handle GET requests to get all categories
        
        Returns:
            Response -- JSON serialized list of categories
        """
        
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer for categories
    """
    class Meta:
        model = Category
        fields = ['id', 'label']
        