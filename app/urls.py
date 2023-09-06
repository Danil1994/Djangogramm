from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # in the future url user has id
    path('user/', views.user_profile, name='user_profile'),
    re_path(r'^post/(?P<pk>[0-9a-f-]+)$', views.PostDetailView.as_view(), name='post-detail'),
    path('post/create', views.post_create, name='post_create'),
    path('explore', views.explore, name='explore'),
]
