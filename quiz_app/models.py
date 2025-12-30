from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    video_url = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_quiz")



class Question(models.Model):
    question_title = models.CharField(max_length=255)
    question_options = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    answer = models.CharField(max_length=500)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="quiz_question")