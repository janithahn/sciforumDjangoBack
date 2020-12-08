from rest_framework import serializers
from comment.models import AnswerComment, PostComment
from vote.models import AnswerCommentVote, PostCommentVote


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
    ownerAvatar = serializers.ImageField(source='owner.profile.profileImg')
    likes = serializers.SerializerMethodField(read_only=True)
    dislikes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = AnswerComment
        fields = ['id', 'answer', 'owner', 'ownerDisplayName', 'ownerAvatar', 'comment', 'created_at', 'updated_at', 'likes', 'dislikes']

    def get_likes(self, obj):
        return AnswerCommentVote.objects.filter(comment_id=obj.id, voteType='LIKE').count()

    def get_dislikes(self, obj):
        return AnswerCommentVote.objects.filter(comment_id=obj.id, voteType='DISLIKE').count()


# POST
class PostCommentSerializer(serializers.ModelSerializer):

    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    ownerDisplayName = serializers.CharField(source='owner.username', read_only=True)
    ownerAvatar = serializers.ImageField(source='owner.profile.profileImg', read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    dislikes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = PostComment
        fields = ['id', 'post', 'owner', 'ownerDisplayName', 'ownerAvatar', 'comment', 'created_at', 'updated_at', 'likes', 'dislikes']

    def get_likes(self, obj):
        return PostCommentVote.objects.filter(comment_id=obj.id, voteType='LIKE').count()

    def get_dislikes(self, obj):
        return PostCommentVote.objects.filter(comment_id=obj.id, voteType='DISLIKE').count()