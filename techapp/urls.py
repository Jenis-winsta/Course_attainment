from . import views
from django.urls import path

urlpatterns=[

    path('',views.login,name='login'),    
    path('login',views.login,name="login1"),    
    path('dashboard',views.dashboard,name='dashboard'),
    path('register',views.register,name='register'),
    path('logout',views.logout, name='logout'), 
    path('index',views.index, name='index'),
    path('maps',views.maps, name='maps'),
    path('result', views.result, name='result'),
    
    # path('get_years/', views.get_years, name='get_years'),
    path('ajax/load-semesters/', views.load_semesters, name='ajax_load_semesters'),
    path('ajax/load-courses/', views.load_courses, name='ajax_load_courses'),



]