from django.db import models
from blog.models import Post
# Create your models here.

class Comment(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
            (STATUS_NORMAL, 'NORMAL'),
            (STATUS_DELETE, 'DELETE')
        )
    target = models.ForeignKey(Post, on_delete = models.DO_NOTHING, verbose_name = 'target')
    content = models.CharField(max_length = 2000, verbose_name = 'content')
    nickname = models.CharField(max_length = 50, verbose_name = 'nick name')
    website = models.URLField(verbose_name = 'website')
    email = models.EmailField(verbose_name = 'email')
    status = models.PositiveIntegerField(default = STATUS_NORMAL,
            choices = STATUS_ITEMS, verbose_name = 'status')
    created_time = models.DateTimeField(auto_now_add = True, verbose_name = 'created time')

    class Meta:
        verbose_name = verbose_name_plural = 'comment'
