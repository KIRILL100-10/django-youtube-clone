from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('profile/delete/', views.profile_delete, name='profile_delete'),
    path('profile/delete/confirm/', views.profile_delete_confirm, name='profile_delete_confirm'),
    path('add_video/', views.add_video, name='video_add'),
    path('video/<int:video_id>/', views.video_detail, name='video_detail'),
    path('video/<int:video_id>/edit/', views.video_edit, name='video_edit'),
    path('video/<int:video_id>/delete/', views.video_delete, name='video_delete'),
    path('video/<int:video_id>/add_comment/', views.add_comment, name='add_comment'),
    path('videos/<int:video_id>/edit_comment/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('video/<int:video_id>/like/', views.like_video, name='like_video'),
    path('channel/<int:channel_id>/subscribe/', views.subscribe_channel, name='subscribe_channel'),
]
