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


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile
    """
    if created:
        UserProfile.objects.create(user=instance)
    # Existing users: just save the profile
    instance.user_profile.save()

class ProfileForm(forms.ModelForm):
    """ Create Profile Form """

    class Meta:
        model = UserProfile
        fields = [
            'image', 'user', 
            'bio', 
        ]