from rest_framework import serializers
from django.contrib.auth import get_user_model
from post.models import Post
from notifications.models import Notification

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class ActionObjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    recipient = UserSerializer(read_only=True)
    actor = UserSerializer(read_only=True)
    unread = serializers.BooleanField(read_only=False)
    public = serializers.BooleanField(read_only=True)
    # target = ActionObjectSerializer(read_only=True)
    verb = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    action_object = ActionObjectSerializer(read_only=True)
    timestamp = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'actor', 'unread', 'public', 'action_object', 'verb', 'description', 'timestamp']