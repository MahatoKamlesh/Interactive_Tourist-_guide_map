from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Homepage
    path('create-buffer/', views.create_buffer, name='create_buffer'),  # Buffer creation endpoint
    path('api/proximity_query/', views.proximity_query, name='proximity_query'),
    path('about/', views.about, name='about'),
    path('documentation/', views.documentation, name='documentation'),
]
