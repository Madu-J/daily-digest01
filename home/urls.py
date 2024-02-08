from . import views
from django.urls import path

urlpatterns = [
    path("", views.PostList.as_view(), name="home"),
    path("news/", views.PostList.as_view(), name="news"),
    path("comments/", views.CommentList.as_view(), name="post_detail"),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('like/<slug:slug>', views.PostLike.as_view(), name='post_like'),
    path('comments/<int:pk>/update/', views.UpdateComment.as_view(), name='update_comment'),
    path('comments/<int:pk>/delete/', views.DeleteComment.as_view(), name='delete_comment'),
    path('addstory/<int:pk>/addstory', views.AddStory.as_view(), name='add_story'),
]