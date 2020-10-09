from django.urls import path
from . import views  


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('profile/<int:user_id>/', views.profile_detail, name='profile_detail'),
    path('cities/', views.cities_index, name='cities_index'),
    path('cities/<int:city_id>/', views.cities_detail, name='cities_detail'),
    # path('cities/<int:city_id>/delete/', views.cities_delete, name='cities_delete'),
    path('profile/<int:user_id>/edit/', views.profile_edit, name='profile_edit'),
    # path('cities/<int:city_id>/assoc_post', views.assoc_post, name='assoc_cities_post'),
    # path('cities/<int:city_id>/deassoc_post', views.deassoc_post, name='deassoc_cities_post'),
    path('accounts/signup/', views.signup, name='signup'),
    path('profile/home/', views.custom_login, name='custom_login'),
]
