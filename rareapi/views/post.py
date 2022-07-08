"""View module for handling requests about posts"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from django.core.exceptions import ValidationError
from rareapi.models import Post, RareUser

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
    
    @action(methods=['get'], detail=False)
    def my_posts(self, request):
        """Get request to display logged-in user's posts on the /posts/my_posts page"""
        user = RareUser.objects.get(user=request.auth.user)
        posts = Post.objects.all()
        posts = posts.filter(user_id=user)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations
        
        Returns:
            Response -- JSON serialized post instance
        """
        user = RareUser.objects.get(user=request.auth.user)
        serializer = CreatePostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        
class PostSerializer(serializers.ModelSerializer):
    """JSON serializer for posts
    """
    class Meta:
        model = Post
        fields = ['id', 'user', 'category', 'title', 'publication_date', 'image_url', 'content', 'tags', 'reactions']
        depth = 2

class CreatePostSerializer(serializers.ModelSerializer):
    """JSON serializer for posts
    """
    class Meta:
        model = Post
        fields = ['id', 'category', 'title', 'publication_date', 'image_url', 'content', 'approved']