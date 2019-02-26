from django.urls import path

from . import views

app_name = 'character'
urlpatterns = [
    path('', views.list, name='index'),
    path('list/', views.list, name='list'),
    path('create_character/', views.create_character, name='create_character'),
    path('details/<uuid:character_id>/', views.details, name='details'),
    path('retire/<uuid:character_id>/', views.retire, name='retire'),
    path('die/<uuid:character_id>/', views.die, name='die'),
    path('resurrect/<uuid:character_id>/', views.resurrect, name='resurrect'),
]
