from django.db import models
from django.contrib.auth.models import User
from post.models import Post
# from django.core.paginator import Paginator

ANSWERS_PER_PAGE = 2


class Answer(models.Model):
    postBelong = models.ForeignKey(Post, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    answerContent = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    up_vote_count = models.IntegerField(default=0, blank=True)

    def get_page(self):
        answers = Answer.objects.filter(postBelong=self.postBelong)
        # paginator = Paginator(answers, ANSWERS_PER_PAGE)
        # print(paginator.page(1).object_list)
        for index, answer in enumerate(answers):
            if answer.id == self.id:
                count = index / ANSWERS_PER_PAGE + 1
                return int(count)
        return None
