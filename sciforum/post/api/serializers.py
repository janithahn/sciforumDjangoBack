from post.models import Post, Visitors, PostImages
from user_profile.models import ProfileViewerInfo
from rest_framework import serializers
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer
from vote.models import PostVote, AnswerVote
from answer.models import Answer
import datetime
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


class PostImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostImages
        fields = ['id', 'post', 'created_at', 'image']


class PostTempImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostImages
        fields = ['id', 'created_at', 'image']


class PostSerializer(serializers.ModelSerializer, TaggitSerializer):

    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    owner = serializers.CharField(source='owner.username', read_only=True)
    tags = TagListSerializerField()
    likes = serializers.SerializerMethodField(read_only=True)
    dislikes = serializers.SerializerMethodField(read_only=True)
    answers = serializers.SerializerMethodField(read_only=True)
    images = PostImagesSerializer(many=True, read_only=True)
    vote_count = serializers.IntegerField(read_only=True)
    # hotness = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'owner', 'title', 'body', 'viewCount', 'created_at', 'updated_at', 'label', 'tags', 'likes', 'dislikes',
                  'vote_count', 'answers', 'hotness', 'images']

    def get_likes(self, obj):
        return PostVote.objects.filter(post_id=obj.id, voteType='LIKE').count()

    def get_dislikes(self, obj):
        return PostVote.objects.filter(post_id=obj.id, voteType='DISLIKE').count()

    def get_answers(self, obj):
        return Answer.objects.filter(postBelong=obj.id).count()

    '''def get_hotness(self, obj):
        answer_count = Answer.objects.filter(postBelong=obj.id).count()
        score = PostVote.objects.filter(post_id=obj.id, voteType='LIKE').count()
        answer_score = 0
        age_in_hours = (datetime.datetime.today().replace(tzinfo=None) - obj.created_at.replace(tzinfo=None)).days * 60
        for answer in Answer.objects.filter(postBelong=obj.id):
            answer_score += AnswerVote.objects.filter(answer=answer, voteType='LIKE').count()

        hotness = ((min(answer_count, 10) * score) / (5 + answer_score)) / ((age_in_hours + 1) ** 1.4)
        return hotness'''


class PostCreateSerializer(TaggitSerializer, serializers.ModelSerializer):

    tags = TagListSerializerField()
    # images = PostImagesSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = ['owner', 'title', 'body', 'tags', 'label']

    '''def create(self, validated_data):
        images_data = validated_data.pop('images')
        post = Post.objects.create(**validated_data)
        for image_data in images_data:
            PostImages.objects.create(post=post, **image_data)
        return post'''


class PostUpdateSerializer(TaggitSerializer, serializers.ModelSerializer):

    tags = TagListSerializerField()
    images = PostImagesSerializer(many=True)

    class Meta:
        model = Post
        fields = ['title', 'body', 'tags', 'label', 'images']


class TopPostsSerializer(serializers.ModelSerializer):

    vote_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'vote_count']