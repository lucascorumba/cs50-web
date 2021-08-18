from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("closed", views.closedIndex, name="closed"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.registerUser, name="register"),
    path("newListing", views.newListing, name="new"),    
    path("watchlist", views.watchlist, name="watch"),
    path("refresh", views.newInput, name="refresh"),
    path("<int:listing>", views.listing, name="listing"),
    path("categories/<str:category>", views.category, name="category")
]
