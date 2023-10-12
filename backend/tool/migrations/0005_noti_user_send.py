# Generated by Django 4.1.3 on 2023-10-08 04:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tool', '0004_alter_noti_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='noti',
            name='user_send',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_send', to=settings.AUTH_USER_MODEL),
        ),
    ]