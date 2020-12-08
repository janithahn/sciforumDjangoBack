from django.db import models
from django.contrib.auth.models import User
from post.models import Post
from answer.models import Answer
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from comment.models import PostComment, AnswerComment


class VoteType(models.TextChoices):
    EMPTY = 'EMPTY'
    LIKE = 'LIKE'
    DISLIKE = 'DISLIKE'


class PostVote(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    voteType = models.CharField(max_length=10, choices=VoteType.choices, default=VoteType.EMPTY)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)

    '''Make post, voteType and owner unique together inorder to avoid 
    same user putting likes on same answer again and again'''
    class Meta:
        unique_together = ('post', 'owner', )


class PostCommentVote(models.Model):
    
    comment = models.ForeignKey(PostComment, on_delete=models.CASCADE)
    voteType = models.CharField(max_length=10, choices=VoteType.choices, default=VoteType.EMPTY)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('comment', 'owner',)


class AnswerVote(models.Model):

    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    voteType = models.CharField(max_length=10, choices=VoteType.choices, default=VoteType.EMPTY)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('answer', 'owner', )


class AnswerCommentVote(models.Model):
    comment = models.ForeignKey(AnswerComment, on_delete=models.CASCADE)
    voteType = models.CharField(max_length=10, choices=VoteType.choices, default=VoteType.EMPTY)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('comment', 'owner',)


# this is the activity model for GenericModel
class CommentVote(models.Model):

    voteType = models.CharField(max_length=10, choices=VoteType.choices, default=VoteType.EMPTY)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    voted_object = GenericForeignKey('content_type', 'object_id')
