from django import forms


from .models import Comment
import mistune



class CommentForm(forms.ModelForm):
    nickname = forms.CharField(
            label = 'Nickname',
            max_length = 50,
            widget = forms.widgets.Input(
                attrs = {'class': 'form-control', 'style': 'width: 60%'}
                )
            )
    email = forms.CharField(
            label = 'Email',
            max_length = 50,
            widget = forms.widgets.EmailInput(
                attrs = {'class': 'form-control', 'style': 'width:60%'}
                )
            )
    website = forms.CharField(
            label = 'Website',
            max_length = 100,
            widget = forms.widgets.URLInput(
                attrs = {'class': 'form-control', 'style': 'width: 60%'}
                )
            )
    content = forms.CharField(
            label = 'Content',
            max_length = 500,
            widget = forms.widgets.Textarea(
                attrs = {'class': 'form-control', 'style': 'width: 60%'}
                )
            )
    

    def clean_content(self):
        content = self.cleaned_data.get('content')
        content = mistune.markdown(content)
        if len(content) < 10:
            raise forms.ValidationError('Too little content')
        return content

    
    class Meta:
        model = Comment
        fields = ['nickname', 'email', 'website', 'content']
