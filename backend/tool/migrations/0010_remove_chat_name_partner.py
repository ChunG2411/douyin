# Generated by Django 4.2.5 on 2023-11-02 07:05

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("tool", "0009_chat_name_partner"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="chat",
            name="name_partner",
        ),
    ]
