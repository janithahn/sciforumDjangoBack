from post.models import Post, Visitors
from user_profile.models import ProfileViewerInfo
from rest_framework import serializers
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer
# from user_profile.profile_api.serializers import ProfileSerializer
# from drf_writable_nested.serializers import WritableNestedModelSerializer

class VisitorSerializer(serializers.ModelSerializer):
    visitDate = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Visitors
        fields = ['post', 'visitorIp', 'visitDate']

class ProfileViewerInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileViewerInfo
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer, TaggitSerializer):

    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    owner = serializers.CharField(source='owner.username', read_only=True)
    tags = TagListSerializerField()

    class Meta:
        model = Post
        fields = ['id', 'owner', 'title', 'body', 'viewCount', 'created_at', 'updated_at', 'tags']

class PostCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['owner', 'title', 'body']

class PostUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['title', 'body']