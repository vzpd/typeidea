from django.db import models 
from django.contrib.auth.models import User



class Category(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
            (STATUS_NORMAL, 'NORMAL'),
            (STATUS_DELETE, 'DELETE')
        )
    name = models.CharField(max_length = 50,verbose_name = 'name') 
    status = models.PositiveIntegerField(default = STATUS_NORMAL, 
        choices = STATUS_ITEMS, verbose_name = 'status') 
    is_nav = models.BooleanField(default = False, verbose_name = 'is_nav') 
    owner = models.ForeignKey(User, on_delete = models.DO_NOTHING, verbose_name = 'owner') 
    created_time = models.DateTimeField(auto_now_add = True, verbose_name = 'created_time') 

    class Meta: 
        verbose_name = verbose_name_plural = 'category'


class Tag(models.Model): 
    STATUS_NORMAL = 1 
    STATUS_DELETE = 0
    STATUS_ITEMS = (
            (STATUS_NORMAL, 'NORMAL'),
            (STATUS_DELETE, 'DELETE')
        )
    name = models.CharField(max_length = 10, verbose_name = 'name')
    status = models.PositiveIntegerField(default = STATUS_NORMAL,
            choices = STATUS_ITEMS, verbose_name = 'status')
    owner = models.ForeignKey(User, on_delete = models.DO_NOTHING, verbose_name = 'owner')
    created_time = models.DateTimeField(auto_now_add = True, verbose_name = 'created_time') 

    
    class Meta: 
        verbose_name = verbose_name_plural = 'tag'


class Post(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = (
            (STATUS_NORMAL, 'NORMAL'),
            (STATUS_DELETE, 'DELETE'),
            (STATUS_DRAFT, 'DRAFT')
        )
    title = models.CharField(max_length = 255, verbose_name = 'title')
    desc = models.CharField(max_length = 1024, blank = True, verbose_name = 'desc')
    content = models.TextField(verbose_name = 'content', help_text = 'content must be type of MarkDown')
    status = models.PositiveIntegerField(default = STATUS_NORMAL,
            choices = STATUS_ITEMS, verbose_name = 'status')
    category = models.ForeignKey(Category, on_delete = models.DO_NOTHING, verbose_name = 'category')
    tag = models.ForeignKey(Tag, on_delete = models.DO_NOTHING, verbose_name = 'tag')
    owner = models.ForeignKey(User, on_delete = models.DO_NOTHING, verbose_name = 'owner')
    owner = models.ForeignKey(User, on_delete = models.DO_NOTHING, verbose_name = 'owner')
    created_time = models.DateTimeField(auto_now_add = True, verbose_name = 'created_time') 
    class Meta:
        verbose_name = verbose_name_plural = 'post'
        ordering = ['-id']
