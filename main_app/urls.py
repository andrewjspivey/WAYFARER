from django.urls import path
from . import views  
# from django.conf.urls import patterns, url


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),

    # PROFILES
    path('accounts/signup/', views.signup, name='signup'),
    path('profile/home/', views.custom_login, name='custom_login'),
    # path('profile/<int:user_id>/', views.profile_detail, name='profile_detail'),
    path('profile/<slug:slug>/', views.profile_detail, name='profile_detail'),
    path('profile/<int:user_id>/edit/', views.profile_edit, name='profile_edit'),
    
    path('cities/', views.cities_index, name='cities_index'),
    path('cities/<int:city_id>/', views.cities_detail, name='cities_detail'),
    # path('cities/<slug:slug>/', views.cities_detail, name='cities_detail'),
    path('posts/<int:post_id>/', views.posts_detail, name='posts_detail'),
    # path('posts/<slug:slug>/', views.posts_detail, name='posts_detail'),
    path('posts/<int:post_id>/delete', views.posts_delete, name='posts_delete'),
    # path('posts/<slug:slug>/delete', views.posts_delete, name='posts_delete'),
    path('posts/<int:post_id>/edit', views.posts_edit, name='posts_edit'),
    # path('posts/<slug:slug>/edit', views.posts_edit, name='posts_edit'),
    path('cities/<int:city_id>/new_post', views.new_post, name='new_post'),
    # path('cities/<slug:slug>/new_post', views.new_post, name='new_post'),
    
    # path('cities/<int:city_id>/delete/', views.cities_delete, name='cities_delete'),
    # path('cities/<int:city_id>/assoc_post', views.assoc_post, name='assoc_cities_post'),
    # path('cities/<int:city_id>/deassoc_post', views.deassoc_post, name='deassoc_cities_post'),
    # path('cities/<int:city_id>/delete/', views.cities_delete, name='cities_delete'),
    
    # patterns('main_app.views', url(r'^simpleemail/(?<emailto>[\w.%+-]+@[A-Za-z0-9.-}+\.[A-Za-z]{2,4})/', 'confirmation_email', name='confirmation_email'),)
    # path('send/', views.send_email, name="send")
]
