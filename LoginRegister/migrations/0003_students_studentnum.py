# Generated by Django 2.1.7 on 2019-03-03 12:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('LoginRegister', '0002_auto_20190221_2021'),
    ]

    operations = [
        migrations.AddField(
            model_name='students',
            name='studentnum',
            field=models.CharField(default=django.utils.timezone.now, max_length=10),
            preserve_default=False,
        ),
    ]
