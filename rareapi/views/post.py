"""View module for handling requests about posts"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from django.core.exceptions import ValidationError
from rareapi.models import Post, RareUser, Comment
from rareapi.views.comment import CommentSerializer

class PostView(ViewSet):
    """Rare posts view"""
    
    def retrieve(self, request, pk):
        """Handle GET request to get single post
        
        Returns:
            Response -- JSON serialized post
        """
        try: 
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post)
            return Response(serializer.data)
        except Post.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
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
        """Get request to display logged-in user's posts on /posts/my_posts page"""
        user = RareUser.objects.get(user=request.auth.user)
        posts = Post.objects.all()
        posts = posts.filter(user_id=user)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    @action(methods=['get'], detail=True)
    def comments(self, request, pk):
        """Get request to display comments on each post
        """
        comments = Comment.objects.all()
        posts = Post.objects.get(pk=pk)
        comments = comments.filter(post_id=posts)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    @action(methods=['get'], detail=False)
    def my_comments(self, request):
        """Get request to display all logged-in user's comments on /posts/my_comments """
        user = RareUser.objects.get(user=request.auth.user)
        comments = Comment.objects.all()
        comments = comments.filter(author=user)
        serializer = CommentSerializer(comments, many=True)
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
    
    def destroy(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        
        
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