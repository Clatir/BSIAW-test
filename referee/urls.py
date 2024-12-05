from django.urls import path
from . import views
urlpatterns = [
    path('sprawozdanie', views.spr_view, name = 'sprawozdanie'),
    path('referee', views.ref_view, name = 'referee'),
    path('kolegium', views.kol_view, name = 'kolegium'),
    path('test', views.klipy_list, name = 'test'),
    path('listameczy',views.listameczy, name = 'listameczy'),
    path('kolmecze',views.kolmecze, name = 'kolmecze'),
    path('mecze/<int:mecz_id>/', views.szczegolymeczu, name='szczegolymeczu'),
    path('kmecze/<int:mecz_id>/', views.szczegolymeczuk, name='szczegolymeczuk'),
    path('sprawozdanie/<int:mecz_id>/',views.sprawozdanie, name = 'sprawozdanie'),
    path('sprawozdaniek/<int:mecz_id>/',views.sprawozdaniek, name = 'sprawozdaniek'),
    path('sgosp/<int:mecz_id>/',views.sgosp, name = 'sgosp'),
    path('sgospk/<int:mecz_id>/', views.sgospk, name='sgospk'),
    path('sgosc/<int:mecz_id>/',views.sgosc, name = 'sgosc'),
    path('sgosck/<int:mecz_id>/', views.sgosck, name='sgosck'),
    path('event/<int:mecz_id>/',views.event, name = 'event'),
    path('eventk/<int:mecz_id>/',views.eventk, name = 'eventk'),
    path('addevent/<int:mecz_id>/',views.addevent, name = 'addevent'),
    path('addzawodnikh/<int:mecz_id>/',views.addzawodnikh, name = 'addzawodnikh'),
    path('addzawodnika/<int:mecz_id>/',views.addzawodnika, name = 'addzawodnika'),
    path('addmecz', views.addmecz, name = 'addmecz'),
    path('editusr', views.editusr, name = 'editusr'),
    path('editusrphon', views.editusrphon, name = 'editusrphon'),

]