# Generated by Django 4.1.7 on 2023-09-11 04:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("tool", "0006_alter_noti_id"),
    ]

    operations = [
        migrations.CreateModel(
            name="Group",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("name", models.TextField(max_length=255)),
                ("create_time", models.DateTimeField(auto_now_add=True)),
                (
                    "member",
                    models.ManyToManyField(
                        blank=True, related_name="group", to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
            options={
                "verbose_name": "Group",
                "db_table": "tb_group",
                "ordering": ["-create_time"],
            },
        ),
        migrations.CreateModel(
            name="SingleChat",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("context", models.TextField(blank=True, null=True)),
                (
                    "image",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to="single_chat/%(sender__username)s_%(receiver__username)s",
                    ),
                ),
                ("status", models.BooleanField(default=False)),
                ("create_time", models.DateTimeField(auto_now_add=True)),
                (
                    "receiver",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="single_receiver",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "sender",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="single_sender",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Single Chat",
                "db_table": "tb_single_chat",
                "ordering": ["-create_time"],
            },
        ),
        migrations.CreateModel(
            name="GroupChat",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("context", models.TextField(blank=True, null=True)),
                (
                    "image",
                    models.FileField(
                        blank=True, null=True, upload_to="group_chat/%(group__id)s"
                    ),
                ),
                ("create_time", models.DateTimeField(auto_now_add=True)),
                (
                    "group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="group_receiver",
                        to="tool.group",
                    ),
                ),
                (
                    "reader",
                    models.ManyToManyField(
                        blank=True,
                        related_name="group_reader",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "sender",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="group_sender",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Group Chat",
                "db_table": "tb_group_chat",
                "ordering": ["-create_time"],
            },
        ),
    ]