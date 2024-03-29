from . import views
from django.urls import path

urlpatterns = [
    path("", views.PostList.as_view(), name="home"),
    path("about/", views.AboutPage.as_view(), name="about"),
    path('profile/<int:pk>', views.UserProfile.as_view(), name='user_profile'),
    path('comments/<int:pk>/update/', views.UpdateComment.as_view(), name='update_comment'),
    path('comments/<int:pk>/delete/', views.DeleteComment.as_view(), name='delete_comment'),
    path('like/<slug:slug>', views.PostLike.as_view(), name='post_like'),
    path('postdetail/<slug:slug>', views.PostDetail.as_view(), name='post_detail'),
]
