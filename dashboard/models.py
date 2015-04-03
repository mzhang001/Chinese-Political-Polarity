from django.db import models

# Create your models here.


class Question(models.Model):
    desc = models.CharField(max_length=300)


class User(models.Model):
    uid = models.IntegerField()
    ip_address = models.CharField(max_length=20, blank=True)
    income = models.CharField(max_length=30, blank=True)
    birth_year = models.IntegerField(null=True)
    is_male = models.NullBooleanField()
    education_background = models.CharField(max_length=20, blank=True)
    time_created = models.DateTimeField(null=True)


class Answer(models.Model):
    question = models.ForeignKey('Question')
    user = models.ForeignKey('User')
    answer = models.IntegerField()
