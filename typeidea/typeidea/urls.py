"""typeidea URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path

from .custom_site import custom_site
from blog.views import post_list, post_detail
from config.views import links

from blog.views import IndexView, CategoryView, TagView, PostDetailView, SearchView, AuthView
from config.views import LinkView
from comment.views import CommentView

from .autocomplete import CategoryAutocomplete, TagAutocomplete
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    url(r'^$', IndexView.as_view(), name = 'index'),
    url(r'^category/(?P<category_id>\d+)/$', CategoryView.as_view(), name = 'category_list'),
    url(r'^tag/(?P<tag_id>\d+)/$', TagView.as_view(), name = 'tag_list'),
    url(r'^auth/(?P<owner_id>\d+)/$', AuthView.as_view(), name = 'auth_list'),
    url(r'^post/(?P<post_id>\d+).html/$', PostDetailView.as_view(), name = 'post_detail'),
    url(r'^comment/$', CommentView.as_view(), name = 'comment'),
    url(r'^category_autocomplete/$', CategoryAutocomplete.as_view(), name = 'category_autocomplete'),
    url(r'^tag_autocomplete/$', TagAutocomplete.as_view(), name = 'tag_autocomplete'),
    url(r'^search/$',SearchView.as_view(), name = 'search_list'),
    url(r'^links/$', LinkView.as_view(), name = 'links'),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^super_admin/', admin.site.urls, name = 'super_admin'),
    url(r'^admin/', custom_site.urls, name = 'admin'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
