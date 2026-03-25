from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class InterviewSession(models.Model):
    CATEGORY_CHOICES = [
        ('tech', 'Technical'),
        ('hr','HR'),
        ('behavioral', 'Behavioral'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    job_role = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    overall_score = models.FloatField(null=True, blank=True)

class Question(models.Model):
    session = models.ForeignKey(InterviewSession, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    order = models.IntegerField()
    generated_at = models.DateTimeField(auto_now_add=True)

class Answer(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE, related_name='answer')
    text = models.TextField()
    ai_feedback = models.TextField(null=True, blank=True)
    score = models.FloatField(null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)