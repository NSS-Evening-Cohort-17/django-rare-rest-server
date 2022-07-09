"""View module for handlign requests for comments"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from django.core.exceptions import ValidationError
from rareapi.models import Comment

class CommentView(ViewSet):
    """Rare comments view"""
    
    def list(self, request):
        """Handle GET requests to get all comments
        
        Returns:
            Response -- JSON serialized post
        """
        
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
     
class CommentSerializer(serializers.ModelSerializer):
    """JSON serializer for comments
    """
    
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_on']
        depth = 3