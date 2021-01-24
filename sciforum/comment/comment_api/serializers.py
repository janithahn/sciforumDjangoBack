from rest_framework import serializers
from comment.models import PostComment, AnswerComment, PostCommentMentions
from vote.models import PostCommentVote, AnswerCommentVote
from notifications.signals import notify


class VoteRelatedField(serializers.RelatedField):
    """
    A custom field to use for the `vote_object` generic relationship.
    """

    def to_representation(self, value):
        """
        Serialize tagged objects to a simple textual representation.
        """
        if isinstance(value, AnswerComment):
            return 'Answer Comment: ' + value.id
        elif isinstance(value, PostComment):
            return 'Post Comment: ' + value.id
        # raise Exception('Unexpected type of vote object')
        return None


# ANSWER
class AnswerCommentSerializer(serializers.ModelSerializer):

    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    ownerDisplayName = serializers.CharField(source='owner.username', read_only=True)
    ownerAvatar = serializers.ImageField(source='owner.profile.profileImg', read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    dislikes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = AnswerComment
        fields = ['id', 'answer', 'post', 'owner', 'ownerDisplayName', 'ownerAvatar', 'comment', 'created_at', 'updated_at', 'likes', 'dislikes']

    def get_likes(self, obj):
        return AnswerCommentVote.objects.filter(comment_id=obj.id, voteType='LIKE').count()

    def get_dislikes(self, obj):
        return AnswerCommentVote.objects.filter(comment_id=obj.id, voteType='DISLIKE').count()


# POST
class PostCommentMentionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostCommentMentions
        fields = ['user']


class PostCommentSerializer(serializers.ModelSerializer):

    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    ownerDisplayName = serializers.CharField(source='owner.username', read_only=True)
    ownerAvatar = serializers.ImageField(source='owner.profile.profileImg', read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    dislikes = serializers.SerializerMethodField(read_only=True)
    post_comment_mentions = PostCommentMentionsSerializer(many=True)

    class Meta:
        model = PostComment
        fields = ['id', 'post', 'owner', 'ownerDisplayName', 'ownerAvatar', 'comment', 'post_comment_mentions', 'created_at', 'updated_at', 'likes', 'dislikes']

    def get_likes(self, obj):
        return PostCommentVote.objects.filter(comment_id=obj.id, voteType='LIKE').count()

    def get_dislikes(self, obj):
        return PostCommentVote.objects.filter(comment_id=obj.id, voteType='DISLIKE').count()

    ''' writing the mentions '''
    def create(self, validated_data):
        mention_data = validated_data.pop('post_comment_mentions')
        comment = PostComment.objects.create(**validated_data)
        for mention in mention_data:
            ''' writing the mentions to the relevant post comment '''
            PostCommentMentions.objects.create(comment=comment, **mention)

            ''' handling the user notification '''
            from_user = None
            request = self.context.get("request")
            if request and hasattr(request, "user"):
                from_user = request.user
            action_object = PostComment.objects.get(id=comment.id)
            message = str(from_user) + ' has mentioned you in a comment'
            to_user = mention['user']
            if from_user.is_authenticated:
                notify.send(sender=from_user, recipient=to_user, verb=message, action_object=action_object)

        return comment
