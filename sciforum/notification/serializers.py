from rest_framework import serializers
from django.contrib.auth import get_user_model
from post.models import Post
from answer.models import Answer
from comment.models import PostComment, AnswerComment
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class PostObjectSerializer(serializers.ModelSerializer):

    notification_type = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'owner', 'notification_type']

    def get_notification_type(self, obj):
        return str(ContentType.objects.get_for_model(obj))


class AnswerObjectSerializer(serializers.ModelSerializer):

    notification_type = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Answer
        fields = ['id', 'postBelong', 'answerContent', 'owner', 'notification_type']

    def get_notification_type(self, obj):
        return str(ContentType.objects.get_for_model(obj))


class PostCommentObjectSerializer(serializers.ModelSerializer):

    notification_type = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = PostComment
        fields = ['id', 'post', 'owner', 'comment', 'notification_type']

    def get_notification_type(self, obj):
        return str(ContentType.objects.get_for_model(obj))


class AnswerCommentObjectSerializer(serializers.ModelSerializer):

    notification_type = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = AnswerComment
        fields = ['id', 'answer', 'post', 'comment', 'owner', 'notification_type']

    def get_notification_type(self, obj):
        return str(ContentType.objects.get_for_model(obj))


class GenericNotificationRelatedField(serializers.RelatedField):

    def to_representation(self, value):

        if isinstance(value, Post):
            return PostObjectSerializer(value).data
        if isinstance(value, Answer):
            return AnswerObjectSerializer(value).data
        if isinstance(value, PostComment):
            return PostCommentObjectSerializer(value).data
        if isinstance(value, AnswerComment):
            return AnswerCommentObjectSerializer(value).data
        return None


class NotificationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    recipient = UserSerializer(read_only=True)
    actor = UserSerializer(read_only=True)
    unread = serializers.BooleanField(read_only=False)
    public = serializers.BooleanField(read_only=True)
    # target = ActionObjectSerializer(read_only=True)
    verb = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    action_object = GenericNotificationRelatedField(read_only=True)
    timestamp = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'actor', 'unread', 'public', 'action_object', 'verb', 'description', 'timestamp']


class NotificationCountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = ['recipient', 'unread']