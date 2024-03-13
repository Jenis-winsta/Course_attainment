# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_file, name='upload_file'),
    path('visualize/', views.visualize_marks, name='visualize_marks'),
    # path('60/', views.marks_gt_60, name='marks_gt_60'),
    # path('80/', views.marks_gt_80, name='marks_gt_80'),
    # path('90/', views.marks_gt_90, name='marks_gt_90'),
    
    

]
