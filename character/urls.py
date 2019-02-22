from django.urls import path

from . import views

app_name = 'character'
urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.list, name='list'),
    path('create_character/', views.create_character, name='create_character'),
    path('details/<int:character_id>/', views.details, name='details'),
]
