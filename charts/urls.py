# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.visualize_scores, name='upload_file'),
    path('visualize/', views.visualization_page, name='visualization_page'),    

]
