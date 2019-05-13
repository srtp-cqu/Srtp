from django.db import models

# Create your models here.
class Students(models.Model):
    name = models.CharField(max_length=20)
    studentnum = models.CharField(max_length=10)
    password = models.CharField(max_length=100)
    imgpath = models.CharField(max_length=80)
    money = models.DecimalField(max_digits=7,decimal_places=2,default=0.00)


class Teachers(models.Model):
    name = models.CharField(max_length=20)
    password = models.CharField(max_length=100)


class Class1(models.Model):
    name = models.CharField(max_length=20)
    studentnum = models.CharField(max_length=10)


class Class2(models.Model):
    name = models.CharField(max_length=20)
    studentnum = models.CharField(max_length=10)


class Drivers(models.Model):
    name = models.CharField(max_length=20)
    password = models.CharField(max_length=100)