from django.urls import path

from main_app import views

urlpatterns = [
    path('', views.IndexListView.as_view(), name='index'),
    path('explore/', views.ExploreView.as_view(), name='explore'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('self_profile/', views.SelfProfileView.as_view(), name='self_profile'),
    path('profile/<int:pk>/', views.SomeoneProfileView.as_view(), name='someone_profile'),
    path('profile/edit/', views.EditProfile.as_view(), name='edit_profile'),
    path('post_detail/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/create/', views.CreatePostView.as_view(), name='post_create'),
    path('post/<int:post_pk>/comment/', views.AddCommentToPostView.as_view(), name='add_comment_to_post'),
    path('<int:pk>/like-dislike/', views.AddLikeDislike.as_view(), name='like-dislike'),
    path('search/', views.SearchResultsView.as_view(), name='search_view'),
    path('profile/<int:pk>/subscribe/', views.SubscribeView.as_view(), name='subscribe'),
    path('last_news/', views.IndexListView.as_view(), name='last_news'),
]
