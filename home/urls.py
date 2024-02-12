from . import views
from django.urls import path

urlpatterns = [
    path("", views.PostList.as_view(), name="home"),
    path("news/", views.PostList.as_view(), name="news"),
    path('like/<slug:slug>', views.PostLike.as_view(), name='post_like'),
    path('comments/<int:pk>/update/', views.UpdateComment.as_view(), name='update_comment'),
    path('comments/<int:pk>/delete/', views.DeleteComment.as_view(), name='delete_comment'),
    path('stories/', views.Story.as_view(), name='stories'),
    path('addstory/', views.AddStory.as_view(), name='add_story'),
    path('myprofile/', views.CommentList.as_view(), name='my_profile'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
]