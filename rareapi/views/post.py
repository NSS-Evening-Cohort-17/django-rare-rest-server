"""View module for handling requests about posts"""
from unicodedata import category
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.core.exceptions import ValidationError
from rareapi.models import Post

class PostView(ViewSet):
    """Rare posts view"""
    
    def list(self, request): 
        """Handle GET requests to get all posts
        
        Returns:
            Response -- JSON serialized list of posts
        """
        
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
class PostSerializer(serializers.ModelSerializer):
    """JSON serializer for posts
    """
    class Meta:
        model = Post
        fields = ('id', 'user', 'category', 'title', 'publication_date', 'image_url', 'content', 'tags', 'reactions')
        depth = 2