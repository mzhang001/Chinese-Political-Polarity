from django.db import models

# Create your models here.


class Question(models.Model):
    text = models.CharField(max_length=300)


class User(models.Model):
    id = models.IntegerField()
    ip_address = models.CharField(max_length=20)
    income = models.CharField(max_length=30)
    birth_year = models.IntegerField()
    is_male = models.BooleanField(default=True)
    education_background = models.CharField(max_length=20)
    time_created = models.DateTimeField()


class Answer(models.Model):
    question = models.ForeignKey('Question')
    user = models.ForeignKey('User')
    answer = models.IntegerField()
