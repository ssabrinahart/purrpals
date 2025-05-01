from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('cats/', views.list_view, name='list'),
    path('cats/<int:id>/', views.detail_view, name='detail'),
    path('cats/new/', views.create_view, name='create'),
    path('logged-out/', views.logout_home_view, name='logged_out'),
    path('search/', views.search_view, name='search'),
    path('login/', views.login_view, name='login'),
    path('posts/<int:post_id>/delete/', views.delete_post_view, name='delete_post'),
    path('posts/<int:post_id>/edit/', views.edit_post_view, name='edit_post'),
    path('posts/<int:post_id>/', views.post_detail_view, name='post_detail'),
    path('posts/<int:post_id>/vote/', views.vote_post, name='vote_post'),
    path('ajax/live-search/', views.live_search_view, name='live_search'),
    path('register/', views.register_view, name='register'),
    path('settings/', views.settings_view, name='settings'),
    path("users/<str:username>/update/", views.update_user_role, name="update_user_role"),
    path('users/', views.user_list_view, name='user_list'),
    path('users/<str:username>/', views.user_profile_view, name='user_profile'),
    path('comment/<int:comment_id>/delete/', views.delete_comment_view, name='delete_comment'),
    path("comments/<int:comment_id>/edit/", views.edit_comment_view, name="edit_comment"),

]
