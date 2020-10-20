from rest_framework import serializers
from vote.models import PostVote, AnswerVote

#ANSWER
class AnswerVoteSerializer(serializers.ModelSerializer):

    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    ownerDisplayName = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = AnswerVote
        fields = ['id', 'answer', 'voteType', 'owner', 'ownerDisplayName', 'created_at']

class AnswerVoteCreateSerializer(serializers.ModelSerializer):

    ''' get_unique_together_validators returns an empty array just to avoid unique together validator '''
    def get_unique_together_validators(self):
        return []

    '''  overriding create method to and update or create functionality to update if the object already exists '''
    def create(self, validated_data):
        owner = validated_data.get('owner', None)
        answer = validated_data.get('answer', None)
        voteType = validated_data.get('voteType', None)
        vote, created = AnswerVote.objects.update_or_create(
            owner=owner,
            answer=answer,
            defaults={"voteType": voteType}
        )
        return vote

    class Meta:
        model = AnswerVote
        fields = ['answer', 'voteType', 'owner']

class AnswerVoteUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnswerVote
        fields = ['voteType']

#POST
class PostVoteSerializer(serializers.ModelSerializer):

    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    ownerDisplayName = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = PostVote
        fields = ['id', 'post', 'voteType', 'owner', 'ownerDisplayName', 'created_at']

class PostVoteCreateSerializer(serializers.ModelSerializer):

    ''' get_unique_together_validators returns an empty array just to avoid unique together validator '''

    def get_unique_together_validators(self):
        return []

    '''  overriding create method to and update or create functionality to update if the object already exists '''

    def create(self, validated_data):
        owner = validated_data.get('owner', None)
        post = validated_data.get('post', None)
        voteType = validated_data.get('voteType', None)
        vote, created = PostVote.objects.update_or_create(
            owner=owner,
            post=post,
            defaults={"voteType": voteType}
        )
        return vote

    class Meta:
        model = PostVote
        fields = ['post', 'voteType', 'owner']

class PostVoteUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostVote
        fields = ['voteType']
