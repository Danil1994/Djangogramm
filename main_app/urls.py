from django.urls import path

from . import views
from .views import SignUpView

urlpatterns = [
    path('', views.index, name='index'),
    path('explore/', views.explore, name='explore'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', views.user_profile, name='self_profile'),
    path('profile/<int:user_id>/', views.view_users_profile, name='view_users_profile'),
    path('profile/edit/', views.EditProfile.as_view(), name='edit_profile'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/create/', views.create_post, name='post_create'),
    path('post/<int:post_pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('post/<int:post_pk>/like/', views.add_like_to_post, name='add_like_to_post'),
    path('search/', views.SearchResultsView.as_view(), name='search_view'),
]
