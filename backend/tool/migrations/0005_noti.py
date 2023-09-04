# Generated by Django 4.1.3 on 2023-09-04 14:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('video', '0008_alter_commentvideo_id_alter_video_music'),
        ('tool', '0004_delete_noti'),
    ]

    operations = [
        migrations.CreateModel(
            name='Noti',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('1', 'like_video'), ('2', 'comment_video'), ('3', 'like_comment'), ('4', 'comment_comment'), ('5', 'follow')], max_length=10)),
                ('context', models.TextField()),
                ('status', models.BooleanField(default=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_noti', to=settings.AUTH_USER_MODEL)),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='video_noti', to='video.video')),
            ],
            options={
                'verbose_name': 'Notification',
                'db_table': 'tb_noti',
                'ordering': ['-create_time'],
            },
        ),
    ]