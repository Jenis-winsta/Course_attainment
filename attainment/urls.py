from django.urls import path
from . import views

from django.urls import path
from . import views

urlpatterns = [
    path('course_attain/', views.course_attain, name='course_attain'),
    # path('generate_table/', views.generate_table, name='generate_table'),
    # path('visualization/', views.visualization, name='visualization'),
    path('courses/', views.courses_by_department_semester, name='courses_by_department_semester'),

]