from django.urls import path
from . import views  
# from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),

    # PROFILES
    path('accounts/signup/', views.signup, name='signup'),
    path('profile/home/', views.custom_login, name='custom_login'),
    path('profile/<slug:slug>/', views.profile_detail, name='profile_detail'),
    path('profile/<int:user_id>/edit/', views.profile_edit, name='profile_edit'),
    
    path('cities/', views.cities_index, name='cities_index'),
    path('cities/<int:city_id>/', views.cities_detail, name='cities_detail'),
    path('cities/<int:city_id>/new_post', views.new_post, name='new_post'),
    # path('cities/<slug:slug>/', views.cities_detail, name='cities_detail'),
    
    path('posts/<int:post_id>/', views.posts_detail, name='posts_detail'),
    path('post/<int:post_id>/comment/', views.add_comments, name='add_comments'),
    path('comments/<int:comment_id>/', views.comments_delete, name="comments_delete"),
    path('posts/<int:post_id>/delete', views.posts_delete, name='posts_delete'),
    path('posts/<int:post_id>/edit', views.posts_edit, name='posts_edit'),

]