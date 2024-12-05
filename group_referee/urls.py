from django.urls import path
from . import views


urlpatterns = [
    path('home', views.home_view, name = 'home'),
    path('set_user', views.set_user_view, name = 'set_user'),
]

