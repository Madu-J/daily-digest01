from django.urls import path
from . import views

urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path('browseposts/', views.PostList.as_view(), name='browse_posts'),
    path('addpost/', views.AddPost.as_view(), name='add_post'),
    path('userposts/',views.UserPost.as_view(), name='user_post'),
    path("about/", views.AboutPage.as_view(), name="about"),
    path('userprofile/<int:pk>', views.UserProfile.as_view(), name='user_profile'),
    path('comments/<int:pk>/update/', views.UpdateComment.as_view(), name='update_comment'),
    path('comments/<int:pk>/delete/', views.DeleteComment.as_view(), name='delete_comment'),
    path('posts/<int:pk>/delete/', views.DeletePost.as_view(), name='delete_post'),
    path('like/<slug:slug>', views.PostLike.as_view(), name='post_like'),
    path('postdetail/<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('posts/<slug:slug>/update/', views.UpdatePost.as_view(), name='update_post'),
    path('profiles/<slug:slug>/update/', views.UpdateProfile.as_view(), name='update_profile'),
]
