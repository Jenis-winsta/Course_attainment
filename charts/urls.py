# urls.py
from django.urls import path
from . import views

<<<<<<< HEAD
urlpatterns = [
    path('upload/', views.visualize_scores, name='upload_file'),
    path('visualize/', views.visualization_page, name='visualization_page'),    
=======
>>>>>>> error

urlpatterns = [
    path('upload/', views.upload_data, name='upload_data'),
    path('visualization/', views.visualization_page, name='visualization_page'),
]
