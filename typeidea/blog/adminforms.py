from django import forms
from dal import autocomplete

from .models import Category, Tag, Post
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class PostAdminForm(forms.ModelForm):
    desc = forms.CharField(widget=forms.Textarea, label = 'SUMMARY', required=False)
    
    category = forms.ModelChoiceField(
            queryset = Category.objects.all(),
            widget = autocomplete.ModelSelect2(url = 'category_autocomplete'),
            label = 'Category',
        )

    tag = forms.ModelMultipleChoiceField(
            queryset = Tag.objects.all(),
            widget = autocomplete.ModelSelect2Multiple(url = 'tag_autocomplete'),
            label = 'Tag',
        )

    content_ck = forms.CharField(widget = CKEditorUploadingWidget(), label = 'Content', required = False)

    content_md = forms.CharField(widget = forms.Textarea(), label = 'Content', required = False)

    content = forms.CharField(widget = forms.HiddenInput(), label = 'Content', required = False)

    class Meta:
        model = Post
        fields = ('category', 'tag', 'title', 'desc', 'content', 'status')


    def __init__(self, instance = None, initial = None, *args, **kwargs):
        print('---------instance:', instance)
        initial = initial or {}
        if instance:
            if instance.is_md:
                initial['content_md'] = instance.content
            else:
                initial['content_ck'] = instance.content

        super().__init__(instance = instance, initial = initial, *args, **kwargs)


    def clean(self):
        is_md = self.cleaned_data.get('is_md')
        if is_md:
            content_field_name = 'content_md'
        else:
            content_field_name = 'content_ck'
        content = self.cleaned_data.get(content_field_name)
        if not content:
            self.add_error(content_field_name,'Required!')
            return
        self.cleaned_data['content'] = content
        print('----------------------cleaned_data-----------------')
        for k, v in self.cleaned_data.items():
            print(k, ':', v)
        print(self.__dict__)
        print('----------------------cleaned_data-----------------')
        return super().clean()



    class Media:
        js = ('js/post_editor.js', 'js/jquery-3.5.1.min.js',)
