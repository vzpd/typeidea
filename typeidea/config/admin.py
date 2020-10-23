from django.contrib import admin
from typeidea.custom_site import custom_site
from typeidea.base_admin import BaseOwnerAdmin
from .models import Link, SideBar
# Register your models here.

@admin.register(Link, site = custom_site)
class LinkAdmin(BaseOwnerAdmin):
    list_display = ('title', 'href', 'status', 'weight', 'owner', 'created_time')
    fields = ('title', 'href', 'status', 'weight')
    


@admin.register(SideBar, site = custom_site)
class SideBarAdmin(BaseOwnerAdmin):
    list_display = ('title', 'display_type', 'content', 'created_time')
    fields = ('title', 'display_type', 'content')

