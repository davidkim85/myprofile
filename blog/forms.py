from django import forms
from django.forms import Textarea

from .models import Comment


class EmailPostForm(forms.Form):
    first_name = forms.CharField(label='first_name',max_length=25)
    last_name = forms.CharField(label='last_name',max_length=25)
    email = forms.EmailField(label='email')
    subject = forms.CharField(label='subject', max_length=50)
    body = forms.CharField(label="body",required=False,widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'name', 'email', 'body']



class SearchForm(forms.Form):
    query = forms.CharField()