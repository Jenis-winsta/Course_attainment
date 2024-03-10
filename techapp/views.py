
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import Group
from django.contrib.auth.models import User, auth
from django.contrib import messages
from users.models import CustomUser
from .models import *
from .forms import *


from django.contrib.auth.decorators import login_required


def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        return render(request, 'index.html',{
            'techapp': Course.objects.all()
        }) 




    
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


# def load_department(request):
#     dept = Semester.objects.values('name').distinct().order_by('name')
#     context={
#         'dept':dept
#     }
#     return render(request, '')



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
    
    
    
# @login_required    
def result(request):
    pso = Programme_Specific_Outcome.objects.all()
    co = Course_Outcome.objects.all()    
    
    context = {
        'program_specific_outcomes': pso,
        'course_outcomes': co,                
    }
    return render(request, 'result.html', context)





def register(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password2=request.POST['password2']
        selected_department_id = request.POST.get('department')  # Get selected department ID
        role = request.POST.get('role')
        
        if password == password2:
            if CustomUser.objects.filter(email=email).exists():
                messages.info(request, 'Email already used')
                return redirect('register')
            elif CustomUser.objects.filter(username=username).exists():
                messages.info(request,'Username already used')
                return redirect('register')
            elif not selected_department_id:
                messages.info(request, 'Please select a department')
                return redirect('register')
            else:
                department = Department.objects.get(pk=selected_department_id)
                user = CustomUser.objects.create_user(username=username,email=email, password=password)
                user.department=department.name
                user.role= role
                user.user_type=role
                user.save()

                 # Add the user to the group with name user_type
                # group_name = '1'
                group_name = user.user_type
                group, created = Group.objects.get_or_create(name=group_name)
                user.groups.add(group)

                messages.success(request, 'Registration successful')
                return redirect('index')
        else: 
            messages.info(request, 'Password not the same')
            return redirect('register')
    else:
        context = {
            'department_options': Department.objects.all(),  # Fetch all departments
        }
        return render(request,'register.html',context)


 



def login(request):
    if request.method=='POST':
        username= request.POST['username']
        password=request.POST['password']

        user= auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            # next_url = request.GET.get('next', '/index')
            # return redirect(next_url)
            return redirect('index')
        else:
            messages.info(request, 'Credential Invalid')
            return redirect('login')
    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


# Create your views here.
# def login(request):
#     return render(request,'login.html')

def dashboard(request):
    return render(request, 'dashboard.html')