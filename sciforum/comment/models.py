from django.contrib.auth.models import User
from post.models import Post
from answer.models import Answer
from django.db import models
# from django.contrib.contenttypes.fields import GenericRelation
# from vote.models import CommentVote


class PostComment(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment


class PostCommentMentions(models.Model):

    comment = models.ForeignKey(PostComment, on_delete=models.CASCADE, null=True, related_name='post_comment_mentions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s: %s' % (self.user, self.comment)


class AnswerComment(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment


class AnswerCommentMentions(models.Model):

    comment = models.ForeignKey(AnswerComment, on_delete=models.CASCADE, null=True, related_name='answer_comment_mentions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s: %s' % (self.user, self.comment)
