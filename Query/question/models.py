from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from answer.models import Answer
from like.models import Like
# Create your models here.


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.CharField(max_length=200)
    answers = GenericRelation(Answer)
    likes = GenericRelation(Like)
    date_posted = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return str(self.question[:50])


    class Meta:
        ordering = ['-date_posted']


    @property
    def owner(self):
        return self.user

