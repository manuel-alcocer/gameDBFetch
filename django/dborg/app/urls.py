from django.urls import path

from . import views

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('regions/', views.regions, name='regions'),
    path('system/', views.systems, name='systems'),
    path('actions/', views.actions, name='actions'),
    path('scan/', views.scan, name='scan'),
    path('addfiles/', views.addFiles, name='addFiles'),
]
