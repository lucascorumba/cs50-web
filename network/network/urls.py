
from django.urls import path

from . import views, utils

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:page>", views.feed, name="feed"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:profile>/<int:page>", views.profile, name="profile"),
    path("following/<int:page>", views.following, name="following"),
    # Fetch call
    path("follow", views.network, name="follow"),
    path("like", views.like, name="like"),
    path("post/<int:post_id>", utils.getPost, name="post"),
    path("change", views.saveChanges, name="change")
]
