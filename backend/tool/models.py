from django.db import models

from user.models import User

# Create your models here.
class SearchRecent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_search")
    text = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-create_time']
        db_table = 'tb_search_recent'
        verbose_name = 'Search recent'

