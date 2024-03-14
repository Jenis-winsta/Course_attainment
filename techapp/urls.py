from . import views
from django.urls import path

urlpatterns=[

    path('',views.login,name='login'),    
    path('login',views.login,name="login1"),    
    path('register',views.register,name='register'),
    path('logout',views.logout, name='logout'), 
    path('index',views.index, name='index'),
    path('maps',views.maps, name='maps'),
    path('result', views.result, name='result'),
    path('ajax/load-semesters/', views.load_semesters, name='ajax_load_semesters'),
    path('ajax/load-courses/', views.load_courses, name='ajax_load_courses'),

    # path('get_years/', views.get_years, name='get_years'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('pso', views.pso, name='pso'),
    path('po', views.po, name='po'),
    path('co', views.co, name='co'),

    path('get_course_outcomes/<int:course_id>/', views.get_course_outcomes, name='get_course_outcomes'),
    path('get_program_specific_outcomes/<int:course_id>/', views.get_program_specific_outcomes, name='get_program_specific_outcomes'),
    path('get_programme_outcomes/<int:course_id>/', views.get_programme_outcomes, name='get_programme_outcomes'),

    path('save_results/', views.save_results, name='save_results'),
    path('save_data/', views.save_data, name='save_data'),
    path('success_page', views.success_page, name='success_page')

]