# Generated by Django 4.2.5 on 2023-11-02 02:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("tool", "0007_alter_message_options"),
    ]

    operations = [
        migrations.CreateModel(
            name="Setup",
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
                ("lang", models.CharField(default="en", max_length=10)),
                ("theme", models.CharField(default="dark", max_length=10)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_setup",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Setup",
                "db_table": "tb_setup",
            },
        ),
    ]
