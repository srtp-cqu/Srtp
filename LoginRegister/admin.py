from django.contrib import admin

# Register your models here.
from LoginRegister import models
admin.site.register(models.Teachers)
admin.site.register(models.Students)