from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from cloudinary.models import CloudinaryField
from django_extensions.db.fields import AutoSlugField
from .validators import textfield_not_empty


STATUS = ((0, "Pending"), (1, "Published"))


class Post(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = AutoSlugField(populate_from='title', unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts")
    description = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    excerpt = models.TextField(blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    featured_image = CloudinaryField('image', default='placeholder')
    likes = models.ManyToManyField(
        User, related_name='blog_likes', blank=True)
    
    class Meta:
        ordering = ['-created_on']
    
    def get_absolute_url(self):
        """Get url after user adds/edits post"""
        return reverse('post_detail', kwargs={'slug': self.slug})
        
    def __str__(self):
        return f"{self.title}"

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
    user = models.OneToOneField(
        User, null=True, on_delete=models.CASCADE, related_name='user_profile') 
    bio = models.TextField(max_length=200)
    website_url = models.CharField(max_length=255, null=True, blank=True,)
    facebook_url = models.CharField(max_length=255, null=True, blank=True,)
    twitter_url = models.CharField(max_length=255, null=True, blank=True,)
    instagram_url = models.CharField(max_length=255, null=True, blank=True,)
    youtube_url = models.CharField(max_length=255, null=True, blank=True,)
    profile_pic = models.ImageField(
        null=True, blank=True, upload_to ="images/profile/")

    
    def __str__(self):
        return  f"Profile {self.user} by {self.bio}"

