from django.urls import path
from . import views

urlpatterns = [
    path('', views.login),
    path('login_process', views.login_process),
    path('register', views.register),
    path('register_process', views.register_process),
    path('wall', views.wall),
    path('logout', views.logout),
    path('add-post', views.add_post),
    path('add-comment', views.add_comment),
]