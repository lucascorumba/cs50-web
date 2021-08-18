from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("seach", views.searchBox, name="search"),
    path("add", views.add, name="add"),
    path("random", views.randomEntry, name="random"),
    path("edit", views.edit, name="edit"),
    path("saveEdit", views.saveEdit, name="save"),
    path("wiki/<str:entry>", views.lookup, name="entry")
]
