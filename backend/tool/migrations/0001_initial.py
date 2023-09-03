# Generated by Django 4.1.3 on 2023-09-03 09:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchRecent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_search', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Search recent',
                'db_table': 'tb_search_recent',
            },
        ),
    ]
