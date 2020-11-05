
from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.urls import reverse
from django.utils.html import format_html
# Register your models here.
from .models import Post, Category, Tag
from .adminforms import PostAdminForm
from typeidea.custom_site import custom_site
from typeidea.base_admin import BaseOwnerAdmin

class PostInline(admin.TabularInline):
    fields = ('title', 'desc')
    extra = 1
    model = Post



@admin.register(Category, site = custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'is_nav', 'owner',  'created_time', 'post_count')
    fields = ('name', 'status', 'is_nav')

#    inlines = [PostInline]
    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = 'ARTICLE COUNT'




@admin.register(Tag, site = custom_site)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'owner', 'created_time')
    fields = ('name', 'status')



class CategoryOwnerFilter(admin.SimpleListFilter):
    title = 'category filter'
    parameter_name = 'owner_category'


    def lookups(self, request, model_admin):
        return Category.objects.filter(owner = request.user).values_list('id','name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id = category_id)
        return queryset

@admin.register(Post, site = custom_site)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm
    list_display = ('title', 'category', 'status', 'owner', 'created_time', 'operator')
    list_display_links = []

    list_filter = [CategoryOwnerFilter]
    search_fields = ['title', 'category']
    
    fieldsets = (
        ('BASE SETTING', {
            'fields': (
                ('title', 'category'),
                'status'
                ),
            }
        ),
        ('CONTENT',{
            'fields':(
                'is_md',
                'desc',
                'content_ck',
                'content_md',
                'content'
                )
            }
        ),
        ('EXTRA INFO', {
            'classes': ('collcapse',),
            'fields': ('tag',),
            }
        )
    )


    
    def operator(self, obj):
        return format_html(
                '<a href = "{}">Edit</a>',
                reverse('cus_admin:blog_post_change', args = (obj.id,))
            )
     
    operator.short_description = 'operat'
    # class Media:
        #css = {
        #        'all': ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css', ),
        #        }
        #js = ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js',



@admin.register(LogEntry, site=custom_site)
class LogEntry(admin.ModelAdmin):
    list_display = ('object_repr', 'object_id', 'action_flag', 'user', 'change_message')
