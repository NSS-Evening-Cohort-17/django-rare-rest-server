"""View module for handling requests about subscriptions"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from django.core.exceptions import ValidationError
from rareapi.models import Subscription

class SubscriptionView(ViewSet):
    """Rare subscriptions view"""
    
    def list(self, request):
        """Handle GET requests to get all subscriptions
        
        Returns:
            Response -- JSON serialized list of subscriptions
        """
        
        subscriptions = Subscription.objects.all()
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data)

class SubscriptionSerializer(serializers.ModelSerializer):
    """JSON serializer for subscriptions
    """
    
    class Meta:
        model = Subscription
        fields = ['id', 'follower', 'author', 'created_on', 'ended_on']
        depth = 2