from django.db import models

# Create your models here.


class Quiz(models.Model):
    title = models.CharField()
    description = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    video_url = models.CharField()


class Question(models.Model):
    question_title = models.CharField()
    question_options = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    answer = models.CharField()
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="quiz_question")