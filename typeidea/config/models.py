from django.db import models
from django.template.loader import render_to_string
from django.contrib.auth.models import User
# Create your models here.

class Link(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 1
    STATUS_ITEMS = (
            (STATUS_NORMAL, 'NORMAL'),
            (STATUS_DELETE, 'DELETE'),
        )
    title = models.CharField(max_length = 50, verbose_name = 'title')
    href = models.URLField(verbose_name = 'href') # default length is 200
    status = models.PositiveIntegerField(default = STATUS_NORMAL, choices = STATUS_ITEMS,
            verbose_name = 'status')
    weight = models.PositiveIntegerField(default = 1,choices = zip(range(1,6), range(1,6)),
            verbose_name = 'weight',help_text = 'more weight,more front')
    owner = models.ForeignKey(User, on_delete = models.DO_NOTHING, verbose_name = 'owner')
    created_time = models.DateTimeField(auto_now_add = True, verbose_name = 'created time')

    class Meta:
        verbose_name = verbose_name_plural = 'Link'


    def __str__(self):
        return self.title


class SideBar(models.Model):
    DISPLAY_HTML = 1
    DISPLAY_LATEST = 2
    DISPLAY_HOT = 3
    DISPLAY_COMMENT = 4
    SIDE_TYPE = (
            (DISPLAY_HTML, 'HTML'),
            (DISPLAY_LATEST, 'LATEST'),
            (DISPLAY_HOT, 'HOT'),
            (DISPLAY_COMMENT, 'COMMENT'),
        ) 
    

    STATUS_SHOW = 1
    STATUS_HIDE = 0
    STATUS_ITMES = (
            (STATUS_SHOW, 'SHOW'),
            (STATUS_HIDE, 'HIDE')
        )
    SIDE_TYPE = (
            (1, 'HTML'),
            (2, 'NEWEST ARTICLE'),
            (3, 'HOTEST ARTICLE'),
            (4, 'NEWEST COMMENTS')
        )
    title = models.CharField(max_length = 50, verbose_name = 'title')
    display_type = models.PositiveIntegerField(default = 1, choices = SIDE_TYPE,
            verbose_name = 'display type')
    content = models.CharField(max_length = 500, blank = True, verbose_name = 'content',
            help_text = 'if display type is not HTML, this can be blank')
    status = models.PositiveIntegerField(default = STATUS_SHOW, choices = STATUS_ITMES,
            verbose_name = 'status')
    owner = models.ForeignKey(User, on_delete = models.DO_NOTHING, verbose_name = 'owner')
    created_time = models.DateTimeField(auto_now_add = True, verbose_name = 'created time')

    class Meta:
        verbose_name = verbose_name_plural = 'SideBar'

    
    def __str__(self):
        return self.title


    @classmethod
    def get_all(cls):
        return cls.objects.filter(status = cls.STATUS_SHOW)


    
    @property
    def content_html(self):
        from blog.models import Post
        from comment.models import Comment

        result = ''
        if self.display_type == self.DISPLAY_HTML:
            result = self.content
        elif self.display_type == self.DISPLAY_LATEST:
            context = {
                    'posts': Post.latest_posts(with_related = False)[:3]
                    }
            result = render_to_string('config/blocks/sidebar_posts.html', context)
        elif self.display_type == self.DISPLAY_HOT:
            context = {
                    'posts': Post.hot_posts()[3:]
                    }
            result = render_to_string('config/blocks/sidebar_posts.html', context)
        elif self.display_type == self.DISPLAY_COMMENT:
            context = {
                    'comments': Comment.objects.filter(status = Comment.STATUS_NORMAL)[:3]
                    }
            result = render_to_string('config/blocks/sidebar_comments.html', context)

        return result
