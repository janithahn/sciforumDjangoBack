from rest_framework import serializers
from vote.models import PostVote, AnswerVote, CommentVote, AnswerCommentVote, PostCommentVote
from generic_relations.relations import GenericRelatedField
from comment.comment_api.serializers import AnswerCommentSerializer, PostCommentSerializer
from comment.models import AnswerComment, PostComment


# ANSWER
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


# ANSWER COMMENT VOTE
class AnswerCommentVoteSerializer(serializers.ModelSerializer):

    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    ownerDisplayName = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = AnswerCommentVote
        fields = ['id', 'comment', 'voteType', 'owner', 'ownerDisplayName', 'created_at']


class AnswerCommentVoteCreateSerializer(serializers.ModelSerializer):

    ''' get_unique_together_validators returns an empty array just to avoid unique together validator '''
    def get_unique_together_validators(self):
        return []

    '''  overriding create method to and update or create functionality to update if the object already exists '''
    def create(self, validated_data):
        owner = validated_data.get('owner', None)
        comment = validated_data.get('comment', None)
        voteType = validated_data.get('voteType', None)
        vote, created = AnswerCommentVote.objects.update_or_create(
            owner=owner,
            comment=comment,
            defaults={"voteType": voteType}
        )
        return vote

    class Meta:
        model = AnswerCommentVote
        fields = ['comment', 'voteType', 'owner']


class AnswerCommentVoteUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnswerCommentVote
        fields = ['voteType']


# POST
class PostVoteSerializer(serializers.ModelSerializer):

    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    ownerDisplayName = serializers.CharField(source='owner.username', read_only=True)
    postTitle = serializers.CharField(source='post.title', read_only=True)

    class Meta:
        model = PostVote
        fields = ['id', 'post', 'postTitle', 'voteType', 'owner', 'ownerDisplayName', 'created_at']


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


# POST COMMENT VOTE
class PostCommentVoteSerializer(serializers.ModelSerializer):

    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    ownerDisplayName = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = PostCommentVote
        fields = ['id', 'comment', 'voteType', 'owner', 'ownerDisplayName', 'created_at']


class PostCommentVoteCreateSerializer(serializers.ModelSerializer):

    ''' get_unique_together_validators returns an empty array just to avoid unique together validator '''
    def get_unique_together_validators(self):
        return []

    '''  overriding create method to and update or create functionality to update if the object already exists '''
    def create(self, validated_data):
        owner = validated_data.get('owner', None)
        comment = validated_data.get('comment', None)
        voteType = validated_data.get('voteType', None)
        vote, created = PostCommentVote.objects.update_or_create(
            owner=owner,
            comment=comment,
            defaults={"voteType": voteType}
        )
        return vote

    class Meta:
        model = PostCommentVote
        fields = ['comment', 'voteType', 'owner']


class PostCommentVoteUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostCommentVote
        fields = ['voteType']

'''
    SEPARATED
'''
from rest_framework.reverse import reverse


class CustomerHyperlink(serializers.HyperlinkedRelatedField):
    # We define these as class attributes, so we don't need to pass them as arguments.
    view_name = 'postcomment-detail'
    queryset = PostComment.objects.all()

    def get_url(self, obj, view_name, request, format):
        print(obj)
        url_kwargs = {
            'pk': obj.pk
        }
        return reverse(view_name, kwargs=url_kwargs, request=request, format=format)

    def get_object(self, view_name, view_args, view_kwargs):
        lookup_kwargs = {
           'pk': view_kwargs['pk']
        }
        return self.get_queryset().get(**lookup_kwargs)


class CommentVoteSerializer(serializers.ModelSerializer):

    voted_object = GenericRelatedField({
        AnswerComment: serializers.HyperlinkedRelatedField(
            queryset=AnswerComment.objects.all(),
            view_name='answercomment-detail',
            lookup_field='id'
        ),
        PostComment: serializers.HyperlinkedRelatedField(
            queryset=PostComment.objects.all(),
            view_name='postcomment-detail',
            lookup_field='id'
        ),
    })

    class Meta:
        model = CommentVote
        fields = ['voted_object', 'voteType', 'owner']
