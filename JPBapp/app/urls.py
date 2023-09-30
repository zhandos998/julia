from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('dashboard', views.dashboard),
    path('solve', views.solve),
    path('datasets', views.datasets),
    path('generate-video', views.generate_video),
    path('get_dataset', views.get_dataset),
    
]