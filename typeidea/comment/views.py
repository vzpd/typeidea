from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.core.exceptions import ValidationError

from .forms import CommentForm




class CommentView(TemplateView):
    http_method_names = ['post']
    template_name = 'comment/result.html'


    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST)
        target = request.POST.get('target')
        error_msg = None
        if comment_form.is_valid():
            if request.user.id is None:
                error_msg = 'Please login first!'
                succeed = False
            else:
                instance = comment_form.save(commit = False)
                instance.target = target
                instance.owner_id = request.user.id
                instance.save()
                succeed = True
                return redirect(target)

        else:
            succeed = False

        context = {
                'error_msg': error_msg,
                'succeed': succeed,
                'form': comment_form,
                'target': target,
            }
        return self.render_to_response(context)
