from django.db import models

# Create your models here.
class Students(models.Model):
    name = models.CharField(max_length=20)
    studentnum = models.CharField(max_length=10)
    password = models.CharField(max_length=100)
    imgpath = models.CharField(max_length=30)


class Teachers(models.Model):
    name = models.CharField(max_length=20)
    password = models.CharField(max_length=100)