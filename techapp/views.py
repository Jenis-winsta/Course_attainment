
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
import json
from .models import *
from .forms import *
from django.contrib.admin.views.decorators import staff_member_required

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages

from django.conf import settings
from django.shortcuts import redirect


def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        return render(request, 'index.html',{
            'techapp': Course.objects.all()
        }) 



# Create your views here.
# def login(request):
#     return render(request,'login.html')







def dashboard(request):
    return render(request, 'dashboard.html', context={'peoples'})
    
def maps(request):
    years = Year.objects.values('id').distinct().order_by('id')
    semesters = Semester.objects.values('name').distinct().order_by('name')
    courses = Course.objects.values('name').distinct()      
    code = Course.objects.values('course_code').distinct()  

    context = {
        'years': years,
        'semesters': semesters,
        'courses': courses,
        'code': code
    }
    return render(request, 'maps.html', context)






def year_course(request):
    years = Year.objects.all()  
    return render(request, 'maps.html', {'years': years})

def load_semesters(request):
    year_id = request.GET.get('year')
    semesters = Semester.objects.filter(year_id=year_id)
    semesters_json = list(semesters.values())
    return JsonResponse({'semesters': semesters_json})

def load_courses(request):
    semester_id = request.GET.get('semester')
    courses = Course.objects.filter(semester_id=semester_id)
    courses_json = list(courses.values())
    return JsonResponse({'courses': courses_json})
    
    
    
    


def result(request):
    pso = Programme_Specific_Outcome.objects.all()
    co = Course_Outcome.objects.all()    
    
    context = {
        'program_specific_outcomes': pso,
        'course_outcomes': co,                
    }
    return render(request, 'result.html', context)


    #     return render(request, 'PurpleTemplate/index.html')
    # else:
    #     return redirect('login')
        


# def button_page(request):
#     return render(request, 'PurpleTemplate/pages/ui-features/buttons.html')


# def dashboard(request):
#     return render(request, 'dashboard.html')


def register(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password2=request.POST['password2']
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already used')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'Username already used')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username,email=email, password=password)
                user.save()
                return redirect('login')

        else: 

            messages.info(request, 'Password not the same')
            return redirect('register')
    else:
        return render(request,'register.html')


 



def login(request):
    if request.method=='POST':
        username= request.POST['username']
        password=request.POST['password']

        user= auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Credential Invalid')
            return redirect('login')
    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('/')