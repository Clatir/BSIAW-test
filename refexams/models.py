from django.db import models

# Create your models here.
class ExamQuestions(models.Model):
    pytanie = models.CharField(max_length=1000)
    poprawna_odpowiedz = models.CharField(max_length=10)
