from django.db import models
from blog.models import Post
from django.contrib.auth.models import User
# Create your models here.

class Comment(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
            (STATUS_NORMAL, 'NORMAL'),
            (STATUS_DELETE, 'DELETE')
        )
    target = models.CharField(max_length = 100, verbose_name = 'target')
    content = models.CharField(max_length = 2000, verbose_name = 'content')
    nickname = models.CharField(max_length = 50, verbose_name = 'nick name')
    website = models.URLField(verbose_name = 'website')
    email = models.EmailField(verbose_name = 'email')
    status = models.PositiveIntegerField(default = STATUS_NORMAL,
            choices = STATUS_ITEMS, verbose_name = 'status', db_index = True)
    owner = models.ForeignKey(User, on_delete = models.DO_NOTHING, verbose_name = 'owner')
    created_time = models.DateTimeField(auto_now_add = True, verbose_name = 'created time')

    class Meta:
        verbose_name = verbose_name_plural = 'comment'

    
    def __str__(self):
        return self.target

    
    @classmethod
    def get_by_target(cls, target):
        return cls.objects.filter(target = target, status = cls.STATUS_NORMAL)
