# Generated by Django 4.2.5 on 2023-10-05 05:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("video", "0002_video_public"),
    ]

    operations = [
        migrations.AddField(
            model_name="music",
            name="name",
            field=models.CharField(default="", max_length=255),
        ),
    ]
