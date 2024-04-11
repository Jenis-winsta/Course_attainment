from django.shortcuts import render, redirect
from .models import *
from techapp.models import *
from charts.models import *
from django.http import JsonResponse
from django.http import HttpResponse, JsonResponse

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






def overall_report(request):
    if request.method == 'POST':
        # Retrieve selected department and passout year from form submission
        dept_id = request.POST.get('department')
        passout_year_id = request.POST.get('passout_year')

        if dept_id and passout_year_id:
            # Retrieve selected department and passout year objects
            selected_department = Department.objects.get(id=dept_id)
            selected_passout_year = PassoutYear.objects.get(id=passout_year_id)

            # Fetch courses for the selected department and passout year
            courses = Course.objects.filter(department=selected_department).order_by('year__name', 'semester__name')
            
            
            # Retrieve all Programme Outcomes (POs) for table header
            programme_outcomes = Programme_Outcome.objects.all()

            # Prepare course data to send to template
            courses_data = []
            po_totals = {po.code: [] for po in programme_outcomes}  # Dictionary to store PO values for averaging
            for course in courses:
                attainment_percentage = AttainmentPercentage.objects.filter(passout_year__year=selected_passout_year.year, course=course).first()
                percent_a = attainment_percentage.attainment_percentage / 3 if attainment_percentage else 0
                po_data = {}
                course_po_relations = Course_Programme_Outcome.objects.filter(course=course)
                for relation in course_po_relations:
                    po_data[relation.programme_outcome.code] = relation.strength
                    po_totals[relation.programme_outcome.code].append(round(relation.strength * percent_a, 2))

                # Assuming course_data structure matches your needs
                # You should customize this based on your Course model and requirements
                course_data = {
                    'year': course.year.name,
                    'semester': course.semester.name,
                    'course_code': course.course_code,
                    'attainment_percentage': attainment_percentage.attainment_percentage if attainment_percentage else 0,  # Modify based on your field name
                    'po_data': {key: round(value * percent_a, 2) for key, value in po_data.items()},
                    
                }
                courses_data.append(course_data)
                
            po_averages = {}
            for po_code, strengths in po_totals.items():
                if strengths:
                    po_averages[po_code] = round(sum(strengths) / len(strengths),2)
                else:
                    po_averages[po_code] = None

            return render(request, 'attainment/overall_report.html', {
                'departments': Department.objects.all(),  # Pass all departments to the template
                'passout_years': PassoutYear.objects.all(),  # Pass all passout years to the template
                'programme_outcomes': programme_outcomes,  # Pass all POs to the template
                'courses': courses_data,  # Pass fetched course data to the template
                'department':selected_department.name,
                'po_averages': po_averages
            })
        else:
            return JsonResponse({'error': 'Invalid parameters'}, status=400)

    # Render the initial form view if not a POST request
    return render(request, 'attainment/overall_report.html', {
        'departments': Department.objects.all(),  # Pass all departments to the template
        'passout_years': PassoutYear.objects.all(),  # Pass all passout years to the template
    })






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
                percent_a = attainment_percentage.attainment_percentage / 3 if attainment_percentage else 0

                if attainment_percentage:
                    po_data = {}
                    course_po_relations = Course_Programme_Outcome.objects.filter(course=course)
                    for relation in course_po_relations:
                        po_data[relation.programme_outcome.code] = relation.strength

                    # First row: "map" for Options column
                    first_row = {
                        'year': course.year.name,
                        'semester': course.semester.name,
                        'course_code': course.course_code,
                        'attainment_percentage': attainment_percentage.attainment_percentage,
                        'po_data': po_data,
                        'options': 'Mapping Strength'  # Value for the "Options" column in the first row
                    }
                    course_data.append(first_row)

                    # Second row: "attain" for Options column and multiplied PO values
                    second_row = {
                        'year': '',  # Empty to skip rendering for common cells
                        'semester': '',  # Empty to skip rendering for common cells
                        'course_code': '',  # Empty to skip rendering for common cells
                        'attainment_percentage': '',  # Value for the "Options" column in the second row
                        'po_data': {key: round(value * percent_a, 2) for key, value in po_data.items()},  # Multiply each PO value by 20
                        'options': 'Course\n Attainment%'  # Value for the "Options" column in the second row
                    }
                    course_data.append(second_row)

            # Render courses in a template (course_table_partial.html)
            context = {'courses': course_data, 'programme_outcomes': Programme_Outcome.objects.all()}
            html_content = render(request, 'attainment/course_table_partial.html', context).content.decode('utf-8')

            # Return JSON response with rendered table HTML
            return JsonResponse({'table_html': html_content})
        else:
            return JsonResponse({'error': 'Invalid parameters'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method or parameters'}, status=400)


