# Generated by Django 4.2.5 on 2023-11-07 02:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("video", "0003_music_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="video",
            name="view",
            field=models.IntegerField(default=0),
        ),
    ]