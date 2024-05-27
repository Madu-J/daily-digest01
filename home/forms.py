from django import forms
from django_summernote.widgets import SummernoteWidget
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Comment, UserProfile, Post
from django.contrib.auth.models import User


class CommentForm(forms.ModelForm):
    """ Create Comment form """
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['body'].widget = forms.Textarea(attrs={'rows': 3})

    class Meta:
        model = Comment
        fields = ('name', 'body',)


class ProfileForm(forms.ModelForm):
    
    class Meta:
            model = UserProfile
            fields = [ 'user', 'bio',
        ]

class PostForm(forms.ModelForm):
    """ Create Post Form """

    class Meta:
        model = Post
        fields = [
            'title', 'method', 
            'description', 'image',
            'publish_time',
        ]