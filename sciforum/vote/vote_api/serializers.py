from rest_framework import serializers
from vote.models import PostVote, AnswerVote

#POST
class PostVoteSerializer(serializers.ModelSerializer):

    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    ownerDisplayName = serializers.CharField(source='owner.username')

    class Meta:
        model = PostVote
        fields = ['id', 'post', 'voteType', 'owner', 'ownerDisplayName', 'created_at']

class PostVoteCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostVote
        fields = ['post', 'voteType', 'owner']

class PostVoteUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostVote
        fields = ['voteType']

#ANSWER
class AnswerVoteSerializer(serializers.ModelSerializer):

    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    ownerDisplayName = serializers.CharField(source='owner.username')

    class Meta:
        model = AnswerVote
        fields = ['id', 'answer', 'voteType', 'owner', 'ownerDisplayName', 'created_at']

class AnswerVoteCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnswerVote
        fields = ['answer', 'voteType', 'owner']

class AnswerVoteUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnswerVote
        fields = ['voteType']