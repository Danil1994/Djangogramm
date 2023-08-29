from django.urls import path
from . import views



urlpatterns = [
    path('', views.index, name='index'),
    path('user/', views.user_profile, name='user_profile'),
    path('post/', views.post_detail, name='post_detail'),
    path('post/create', views.post_create, name='post_create'),
]
