from django.urls import path

from . import views

app_name = 'character'
urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.list, name='list'),
    path('details/<int:character_id>/', views.details, name='details'),
]
