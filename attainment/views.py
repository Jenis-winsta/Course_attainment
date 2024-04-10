from django.shortcuts import render, redirect
from .models import *
from techapp.models import *
from charts.models import *
from django.http import JsonResponse

# Create your views here.
def course_attain(request):
    departments = Department.objects.all()
    semesters = Semester.objects.all()
    passout_years = PassoutYear.objects.all()


    context = {
        'departments': departments,
        'semesters': semesters,
        'passout_years': passout_years
    }
    
    return render(request, 'attainment/course_attainment.html', context)







def courses_by_department_semester(request):
    if request.method == 'POST':
        dept_id = request.POST.get('dept_id')
        sem_id = request.POST.get('sem_id')
        passout_year = request.POST.get('passout_year')

        if dept_id and sem_id and passout_year:
            # Fetch courses based on department, semester, and passout year
            courses = Course.objects.filter(department_id=dept_id, semester_id=sem_id)

            # Prepare data for rendering
            course_data = []
            for course in courses:
                attainment_percentage = AttainmentPercentage.objects.filter(passout_year__year=passout_year, course=course).first()
                if attainment_percentage:
                    po_data = []
                    course_po_relations = Course_Programme_Outcome.objects.filter(course=course)
                    for relation in course_po_relations:
                        po_data.append({
                            'po_code': relation.programme_outcome.code,
                            'strength': relation.strength
                        })
                    course_data.append({
                        'year': course.year.name,
                        'semester': course.semester.name,
                        'course_code': course.course_code,
                        'attainment_percentage': attainment_percentage.attainment_percentage,
                        'po_data': po_data
                    })

                    print(po_data)

            # Render courses in a template (e.g., course_table_partial.html)
            context = {'courses': course_data}
            rendered_table = render(request, 'attainment/course_table_partial.html', context).content.decode('utf-8')

            # Return JSON response with rendered table HTML
            return JsonResponse({'table_html': rendered_table})
        else:
            return JsonResponse({'error': 'Invalid parameters'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method or parameters'}, status=400)
