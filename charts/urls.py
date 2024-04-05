# urls.py
from django.urls import path
from . import views


urlpatterns = [
    path('upload/', views.upload_data, name='upload_data'),
    path('visualization/', views.visualization_page, name='visualization_page'),
]
