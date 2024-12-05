from django.urls import path
from . import views
urlpatterns = [
    path('egzamin', views.egzamin, name = 'egzamin'),
    path('wynik',views.wynik, name = 'wynik'),
]