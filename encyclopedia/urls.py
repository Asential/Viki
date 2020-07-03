from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"), 
    path("wiki/<entry>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("new", views.new, name="new"),
    path("submit", views.submit, name="submit"),
    path("edit/<title>", views.edit, name="edit"),
    path("save/<title>", views.save, name="save"),
    path("random", views.rand, name="random")
]
