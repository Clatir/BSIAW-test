from django.urls import path
from . import views


urlpatterns = [
    path('signup', views.signup, name = 'signup'),
    path('login', views.login_view, name = 'login'),
    path('login/<str:username>', views.main_page_view, name='main_page'), 
    path('logout', views.logout_view, name = 'logout'),

    path('reset_password/', views.reset_password_view , name='reset_password'),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm_view, name="password_reset_confirm"),
    path('home', views.home_view, name = 'home'),
]

