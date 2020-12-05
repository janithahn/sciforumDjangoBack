from rest_framework import serializers
from comment.models import AnswerComment, PostComment


# ANSWER
class AnswerCommentSerializer(serializers.ModelSerializer):

    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    ownerDisplayName = serializers.CharField(source='owner.username', read_only=True)
    ownerAvatar = serializers.ImageField(source='owner.profile.profileImg')

    class Meta:
        model = AnswerComment
        fields = ['id', 'answer', 'owner', 'ownerDisplayName', 'ownerAvatar', 'comment', 'created_at']


# POST
class PostCommentSerializer(serializers.ModelSerializer):

    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    ownerDisplayName = serializers.CharField(source='owner.username', read_only=True)
    ownerAvatar = serializers.ImageField(source='owner.profile.profileImg')

    class Meta:
        model = PostComment
        fields = ['id', 'post', 'owner', 'ownerDisplayName', 'ownerAvatar', 'comment', 'created_at']