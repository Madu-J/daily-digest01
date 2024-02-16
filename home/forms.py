from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import Comment, UserProfile


class CommentForm(forms.ModelForm):
    """ Create Comment form """
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['body'].widget = forms.Textarea(attrs={'rows': 3})

    class Meta:
        model = Comment
        fields = ('name', 'body',)


class ProfileForm(forms.ModelForm):
    """ Create Profile Form """
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget = forms.Textarea(attrs={'rows': 3})

    class Meta:
        """
        Get profile model, choose fields to display and add summernote widget
        """
        model = UserProfile
        fields = [
            'user',
            'bio',
            ]
        widgets = {
            'method': SummernoteWidget(),
            'ingredients': SummernoteWidget(),
        }
      