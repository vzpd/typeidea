from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q, F
from django.contrib.auth.models import User
from .models import Post, Tag, Category
from config.models import SideBar

from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from comment.forms import CommentForm
from comment.models import Comment


from datetime import date
from django.core.cache import cache

def post_list(request, category_id = None, tag_id = None):
    tag = None
    category = None

    if tag_id:
        post_list, tag = Post.get_by_tag(tag_id)
    elif category_id:
        post_list, category = Post.get_by_category(category_id)
    else:
        post_list = Post.latest_posts()

    context = {
            'category': category,
            'tag': tag,
            'post_list': post_list,
            'sidebars': SideBar.get_all()
        }
    context.update(Category.get_navs())
        
    return render(request, 'blog/list.html', context)



def post_detail(request, post_id):
    #return HttpResponse('detail')
    try:
        post = Post.objects.get(id = post_id)
    except Post.DoesNotExist:
        post = None
    context = {
            'post': post,
            'sidebars': SideBar.get_all()
            }
    context.update(Category.get_navs())
    return render(request, 'blog/detail.html', context)



class CommonViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'sidebars': SideBar.get_all(),
            })
        context.update(Category.get_navs())
        return context



class IndexView(CommonViewMixin, ListView):
    queryset = Post.latest_posts()
    paginate_by = 3
    context_object_name = 'post_list'
    template_name = 'blog/list.html'




class SearchView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
                'keyword': self.request.GET.get('keyword','')
                }
            )
        return context

    
    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get('keyword')
        print('keyword:%s'%{keyword})
        if keyword:
            return queryset.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword))
        else:
            return queryset



class AuthView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        owner_id = self.kwargs.get('owner_id')
        owner = User.objects.get(id= owner_id).username
        context.update({
                'owner': owner
                }
            )

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        owner_id = self.kwargs.get('owner_id')
        return queryset.filter(owner_id=owner_id)



class CategoryView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk = category_id)
        context.update({
            'category': category,
            })
        return context


    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id = category_id)




class TagView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag, pk = tag_id)
        context.update({
            'tag': tag,
            })
        return context


    def get_queryset(self):
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tag__id = tag_id)




class PostDetailView(CommonViewMixin, DetailView):
    queryset = Post.latest_posts()
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'comment_form': CommentForm,
            'comment_list': Comment.get_by_target(self.request.path)
            }
        )
        return context
    

    def get(self,request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.handle_visited()
        return response


    def handle_visited(self):
        increase_pv = False
        increase_uv = False
        uid = self.request.uid
        pv_key = 'pv:%s:%s' % (uid, self.request.path)
        uv_key = 'uv:%s:%s:%s' % (uid, str(date.today()), self.request.path)
        if not cache.get(pv_key):
            increase_pv = True
            cache.set(pv_key, 1, 60 * 1)

        if not cache.get(uv_key):
            increase_uv = True
            cache.set(uv_key, 1, 60 * 60 * 24)

        if increase_pv and increase_uv:
            Post.objects.filter(pk = self.object.id).update(pv=F('pv') + 1, uv = F('uv') + 1)
        elif increase_pv:
            Post.objects.filter(pk = self.object.id).update(pv=F('pv') + 1)
        elif increase_uv:
            Post.objects.filter(pk = self.object.id).update(uv = F('uv') + 1)
