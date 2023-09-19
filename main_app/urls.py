from django.urls import path, re_path

from . import views
from .views import SignUpView

urlpatterns = [
    path('', views.index, name='index'),
    path('explore', views.explore, name='explore'),
    path('signup/', SignUpView.as_view(), name='signup'),
    # in the future url user has id
    path('profile/', views.user_profile, name='user_profile'),
    path('profile/edit/', views.EditProfile.as_view(), name='edit_profile'),
    re_path(r'^post/(?P<pk>[0-9]+)$', views.post_detail, name='post_detail'),
    path('post/create/', views.create_post, name='post_create'),
    re_path(r'^post/(?P<post_pk>[0-9]+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),
    path('post/<int:post_pk>/like/', views.add_like_to_post, name='add_like_to_post'),
    path('search/', views.SearchResultsView.as_view(), name='search_view'),

]
