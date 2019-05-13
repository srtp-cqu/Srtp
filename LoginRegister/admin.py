from django.contrib import admin

# Register your models here.
from LoginRegister import models
admin.site.register(models.Teachers)
admin.site.register(models.Students)
admin.site.register(models.Class1)
admin.site.register(models.Class2)
admin.site.register(models.Drivers)