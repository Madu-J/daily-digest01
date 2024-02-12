from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import Comment, Story

class CommentForm(forms.ModelForm):
    """ Create Comment form """
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['body'].widget = forms.Textarea(attrs={'rows': 3})

    class Meta:
        model = Comment
        fields = ('name', 'body',)


class StoryForm(forms.ModelForm):
    """ Create Story form """
    def __init__(self, *args, **kwargs):
        super(StoryForm, self).__init__(*args, **kwargs)
        self.fields['body'].widget = forms.Textarea(attrs={'rows': 3})

    class Meta:
        """
        Get story model, choose fields to display
        """
        model = Story
        fields = ('user', 'post', 'body')
