from django.urls import include, path, re_path

from . import views

urlpatterns = [
    path('one/', views.github, name ="p1")
]