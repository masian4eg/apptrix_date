# Generated by Django 4.0.2 on 2022-02-19 15:21

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profiles', '0002_relationship'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='match',
            field=models.ManyToManyField(blank=True, related_name='match', to=settings.AUTH_USER_MODEL),
        ),
    ]