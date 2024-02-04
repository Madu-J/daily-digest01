from . import views
from django.urls import path

urlpatterns = [
    path("", views.PostList.as_view(), name="home"),
    path("", views.PostList.as_view(), name="news"),
    path("", views.PostList.as_view(), name="tech"),
    path("", views.PostList.as_view(), name="sports"),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('like/<slug:slug>', views.PostLike.as_view(), name='post_like'),
    path('comments/<int:pk>/update/', views.UpdateComment.as_view(), name='update_comment'),
    path('comments/<int:pk>/delete/', views.DeleteComment.as_view(), name='delete_comment'),
]