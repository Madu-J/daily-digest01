from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from cloudinary.models import CloudinaryField

STATUS = ((0, "Draft"), (1, "Published"))


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts")
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    featured_image = CloudinaryField('image', default='placeholder')
    excerpt = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(User, related_name='blog_likes', blank=True)
    comments = models.ManyToManyField(User, related_name='post_comments', blank=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def number_of_likes(self):
        return self.likes.count()


class Comment(models.Model):
    """Comment model"""
    post = models.ForeignKey(Post, 
    on_delete=models.CASCADE, related_name='comment')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Comment {self.name} by {self.name}"

        
class UserProfile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE) 
    bio = models.TextField()
    profile_pic = models.ImageField(null=True, blank=True, upload_to ="images/profile/")
    website_url = models.CharField(max_length=255, null=True, blank=True,)
    facebook_url = models.CharField(max_length=255, null=True, blank=True,)
    twitter_url = models.CharField(max_length=255, null=True, blank=True,)
    instagram_url = models.CharField(max_length=255, null=True, blank=True,)
    youtube_url = models.CharField(max_length=255, null=True, blank=True,)
    
    def __str__(self):
        return  f"Profile {self.user} by {self.bio}"


def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile
    """
    if created:
        UserProfile.objects.create(user=instance)
    # Existing users: just save the profile
    instance.userprofile.save()