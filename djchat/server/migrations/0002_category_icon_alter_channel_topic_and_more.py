# Generated by Django 5.0.6 on 2024-06-15 12:04

import server.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("server", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="icon",
            field=models.FileField(
                blank=True, null=True, upload_to=server.models.category_icon_upload_path
            ),
        ),
        migrations.AlterField(
            model_name="channel",
            name="topic",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name="server",
            name="description",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name="server",
            name="member",
            field=models.ManyToManyField(
                related_name="server_members", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
