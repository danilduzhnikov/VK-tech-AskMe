from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.query import QuerySet

from typing import TypeVar, Generic

from django.conf import settings

T = TypeVar('T')

class CustomUser(AbstractUser):
    login = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.username

class TagsManager(Generic[T], models.Manager):
    def get_popular(self):
        return self.order_by('-views')[:8].values_list('name', flat=True)

    def get_questions_tags(self):
        return self.filter

class QuestionManager(Generic[T], models.Manager):
    def get_new_questions(self):
        return self.order_by('-created_at')

    def get_hot_questions(self):
        return self.order_by('-views')

class QuestionLikeManager(Generic[T], models.Manager):
    def is_user_liked_question(self, user: CustomUser, question_id: int) -> bool:
        return self.filter(user=user, question_id=question_id).exists()
    def get_count_likes_question(self, question_id: int) -> int:
        likes = self.filter(question=question_id)
        return likes.count()

class AnswerManager(Generic[T], models.Manager):
    def get_answers(self, question_id: int) -> QuerySet[T]:
        return self.filter(question_id=question_id)

class AnswerLikeManager(Generic[T], models.Manager):
    def get_count_likes_answer(self, answer_id):
        likes = self.filter(answer=answer_id)
        return likes.count()

class QuestionTagManager(Generic[T], models.Manager):
    def get_question_tags(self, question_id):
        return self.filter(question=question_id)

    def get_questions_per_tag(self, tag:str) -> QuerySet[T]:
        return Question.objects.filter(
            questiontag__tag__name=tag
        ).distinct()

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, default='avatars/default.jpeg')
    description = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)

    objects = TagsManager()
    def __str__(self):
        return self.name

class Question(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='questions_avatars/', null=True, blank=True)
    title = models.CharField(max_length=100)
    text = models.TextField()
    views = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = QuestionManager()

    def __str__(self):
        return self.title

class QuestionTag(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    objects = QuestionTagManager()

    def __str__(self):
        return f"question {self.question.id} + tag {self.tag.id}"

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AnswerManager()

    def __str__(self):
        return self.question.title


class AnswerLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    objects = AnswerLikeManager()

    class Meta:
        unique_together = ('user', 'answer')

class QuestionLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    objects = QuestionLikeManager()

    class Meta:
        unique_together = ('user', 'question')