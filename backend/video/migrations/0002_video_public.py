# Generated by Django 4.2.5 on 2023-10-05 02:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("video", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="video",
            name="public",
            field=models.BooleanField(default=True),
        ),
    ]