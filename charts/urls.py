# urls.py
from django.urls import path
from . import views

 

urlpatterns = [
    path('upload/', views.upload_data, name='upload_data'),
    # path('visualization/', views.visualization_page, name='visualization_page'),
    path('visualization/', views.visualization, name='visualization'),

    path('ajax/load-semesters/', views.load_semesters, name='ajax_load_semesters'),
    path('ajax/load-courses/', views.load_courses, name='ajax_load_courses'),
]
