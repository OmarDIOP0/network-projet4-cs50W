
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new-post",views.new_post_view, name="new-post"),
    # path('my-profile', views.my_profile_view, name="my-profile"),
    path('profile-view/<str:username>/', views.profile_view, name="profile-view"),
    path("follow/<str:username>/", views.follow, name="follow"),
    path("unfollow/<str:username>/", views.unfollow, name="unfollow"),
    path("following_view", views.following_view, name="following_view"),
    path('edit-post/<int:post_id>/', views.edit_post, name='edit-post'),
    path('toggle-like/<int:post_id>/', views.toggle_like, name='toggle-like'),
]
