# # views.py
# import pandas as pd
# import plotly.express as px
# from django.shortcuts import render, redirect
# from django.http import HttpResponse, HttpResponseRedirect
# # from .forms import UploadForm
# from .models import *
# from django.db.models import Avg
# from techapp.models import *
# from django.urls import reverse




# def handle_excel_file(file, year_of_file, course_code):
#     # Load Excel file into Pandas DataFrame
#     df = pd.read_excel(file)

#     course = Course.objects.get(course_code=course_code)
#     # Create File_Description object
#     file_desc = File_Description.objects.get(year_of_file=year_of_file, course=course)
    
#     # Rename the first four headers
#     df.columns = ['name', 'cia_marks', 'semester_marks', 'total_marks'] + list(df.columns[4:])
    
#     # Process and save data to the database
#     process_data(df, file_desc)


# def process_data(df, file_desc):
#     # Iterate through DataFrame rows and save to database
#     for index, row in df.iterrows():
#         Student.objects.create(
#             name=row['name'],
#             cia_marks=row['cia_marks'],
#             semester_marks=row['semester_marks'],
#             total_marks=row['total_marks'],
#             file_desc=file_desc
#         )



# def upload_data(request):
#     years =  File_Description.objects.values_list('year_of_file', flat=True).distinct()
#     course_codes = File_Description.objects.values_list('course__course_code', flat=True).distinct()

#     context={
#         'years': years, 
#         'course_codes': course_codes
#     }
#     return render(request, 'charts/upload_form.html', context)





# def visualization(request):
#     years = File_Description.objects.values_list('year_of_file', flat=True).distinct()

#     individual_graphs = {}
#     trend_graphs = {}

#     if request.method == 'POST':
#         file = request.FILES['file']
        
#         # You can access other form data like this:
#         year_of_file = request.POST.get('year_of_file')
#         course_code = request.POST.get('course_code')

#         # Assuming the uploaded file is in Excel format
#         if file.name.endswith('.xlsx') or file.name.endswith('.xls'):
#             # print("hello")
#             df = pd.read_excel(file)
#             handle_excel_file(file, year_of_file, course_code)

#         # print("reached post of visualization")
#         selected_year = request.POST.get('year_of_file')
#         selected_course_code = request.POST.get('course_code')
#         # print(selected_course_code)
#         # print(selected_year)

#         if selected_year is not None and selected_course_code is not None:
#             course = Course.objects.get(course_code=selected_course_code)
#             # Create File_Description object
#             file_desc = File_Description.objects.get(year_of_file=selected_year, course=course)
            
#             # file_desc = File_Description.objects.get(year_of_file=selected_year, course_code=selected_course_code)

#             students = Student.objects.filter(file_desc=file_desc)

#             # Generate individual graph for the selected year
#             score_ranges = [i * 10 for i in range(11)]
#             score_counts = [students.filter(total_marks__range=(start, start + 9)).count() for start in score_ranges]
#             individual_graph = px.bar(x=score_ranges, y=score_counts, labels={'x': 'Score Range', 'y': 'Number of Students'})
#             individual_graph.update_layout(title=f'Student Scores for {selected_year}', xaxis_title='Score Range', yaxis_title='Number of Students')
#             individual_graphs[selected_year] = individual_graph.to_html(full_html=False)

#             # Compare data year-wise
#             gte_avg_counts = []
#             lt_avg_counts = []

            

#             # Inside the loop where you're calculating average total marks
#             for year in years:
#                 year_file_desc = File_Description.objects.get(year_of_file=year, course=course)
#                 year_students = Student.objects.filter(file_desc=year_file_desc)
#                 avg_total_marks = year_students.aggregate(avg_total_marks=Avg('total_marks'))['avg_total_marks']
#                 if avg_total_marks is not None:
#                     gte_avg_count = year_students.filter(total_marks__gte=avg_total_marks).count()
#                     lt_avg_count = year_students.filter(total_marks__lt=avg_total_marks).count()
#                     gte_avg_counts.append(gte_avg_count)
#                     lt_avg_counts.append(lt_avg_count)
#                 else:
#                     # Handle case where no students exist for the year
#                     gte_avg_counts.append(0)
#                     lt_avg_counts.append(0)


#             # Generate trend graph
#             trend_graph = px.bar(x=[str(year) for year in years], y=[lt_avg_counts, gte_avg_counts], labels={'x': 'Year', 'y': 'Count'}, width=800)
#             trend_graph.update_layout(title='Year-wise Comparison of Student Scores', xaxis_title='Year', yaxis_title='Count')
#             trend_graphs[selected_year] = trend_graph.to_html(full_html=False)

#     return render(request, 'charts/visualize_scores.html', {'years': years, 'individual_graphs': individual_graphs, 'trend_graphs': trend_graphs})



import pandas as pd
import plotly.express as px
from django.shortcuts import render, redirect
from django.db.models import Avg
from .models import *
from techapp.models import Course
import plotly.graph_objects as go
from django.http import HttpResponse, JsonResponse
from techapp.models import *

# from .utils import handle_excel_file
def upload_data(request):
    # years = File_Description.objects.values_list('year_of_file', flat=True).distinct()
    # course_codes = Course.objects.values_list('course_code', flat=True).distinct()
    years = Year.objects.all()
    departments = Department.objects.all()
    passout_year= PassoutYear.objects.all()
    

    if request.method == 'POST':
        file = request.FILES.get('file')
        course_code = request.POST.get('courses')
        passout_year = request.POST.get('passout_year')

        if file and file.name.endswith(('.xlsx', '.xls')) and passout_year and course_code:
            handle_excel_file(file, passout_year, course_code)
            return HttpResponse("Data saved successfully.")

    return render(request, 'charts/upload_form.html', {
        'passout_years': PassoutYear.objects.all(),
        'years': years,
        'departments': departments,
        
    })


def handle_excel_file(file, passout_year, course_code):
    try:
        # Retrieve PassoutYear instance
        passout_year_instance = PassoutYear.objects.get(year=passout_year)

        # Retrieve Course instance
        course = Course.objects.get(pk=course_code)

        # Check if there is an existing File_Description for the same course and passout year
        try:
            file_desc = File_Description.objects.get(passout_year=passout_year_instance, course=course)
        except File_Description.DoesNotExist:
            file_desc = None
        
        # Delete existing File_Description and related Student instances if found
        if file_desc:
            Student.objects.filter(file_desc=file_desc).delete()
            file_desc.delete()

        # Create new File_Description
        file_desc = File_Description.objects.create(passout_year=passout_year_instance, course=course)

        # Load Excel file into Pandas DataFrame
        df = pd.read_excel(file)

        # Rename the first four headers
        df.columns = ['name', 'cia_marks', 'semester_marks', 'total_marks'] + list(df.columns[4:])

        # Process and save data to the database
        for _, row in df.iterrows():
            Student.objects.create(
                name=row['name'],
                cia_marks=row['cia_marks'],
                semester_marks=row['semester_marks'],
                total_marks=row['total_marks'],
                file_desc=file_desc
            )

    except PassoutYear.DoesNotExist:
        print("Passout year does not exist")  # Handle the case where the passout year does not exist
    except Course.DoesNotExist:
        print("Course does not exist")  # Handle the case where the course does not exist

#*commented by you


# def handle_excel_file(file, passout_year, course_code):
#     try:
#         print("reached")
#         print(passout_year)
#         print(course_code)
#         passout_year_instance = PassoutYear.objects.get(year=passout_year)

#         course = Course.objects.get(pk=course_code)
#         file_desc, _ = File_Description.objects.get_or_create(passout_year=passout_year_instance, course=course)

#         # Load Excel file into Pandas DataFrame
#         df = pd.read_excel(file)

#         # Rename the first four headers
#         df.columns = ['name', 'cia_marks', 'semester_marks', 'total_marks'] + list(df.columns[4:])

#         # Process and save data to the database
#         for _, row in df.iterrows():
#             Student.objects.create(
#                 name=row['name'],
#                 cia_marks=row['cia_marks'],
#                 semester_marks=row['semester_marks'],
#                 total_marks=row['total_marks'],
#                 file_desc=file_desc
#             )
#     except Course.DoesNotExist:
#         print("no course")  # Handle the case where the course does not exist






def load_semesters(request):
    year_id = request.GET.get('year')
    semesters = Semester.objects.filter(year_id=year_id)
    semesters_json = list(semesters.values())
    return JsonResponse({'semesters': semesters_json})

def load_courses(request):
    # department_id = request.GET.get('department')
    semester_id = request.GET.get('semester')
    courses = Course.objects.filter(semester_id=semester_id)
    courses_json = list(courses.values())
    return JsonResponse({'courses': courses_json})


from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import File_Description, Student, Year, Semester, Course, Department




def visualization(request):
    # Fetch distinct passout years from File_Description
    passout_years = PassoutYear.objects.all()

    # Fetch distinct courses from File_Description
    courses = File_Description.objects.select_related('course').values_list('course__id', 'course__course_code').distinct()

    if request.method == 'GET':
        selected_passout_year = request.GET.get('passout_year_select')
        selected_course_id = request.GET.get('course_select')


        if selected_passout_year and selected_course_id:
            try:
                # Retrieve file description for the selected passout year and course
                file_desc = File_Description.objects.get(passout_year_id=selected_passout_year, course_id=selected_course_id)

                # Retrieve course name based on selected_course_id
                selected_course_name = file_desc.course.course_code

                # Retrieve students data for the selected passout year and course
                students = Student.objects.filter(file_desc=file_desc)

                # Calculate average total marks for the selected passout year and course
                avg_total_marks = students.aggregate(avg_total_marks=Avg('total_marks'))['avg_total_marks']

                if avg_total_marks is not None:
                    # Calculate counts of students scoring above and below average
                    above_avg_count = students.filter(total_marks__gte=avg_total_marks).count()
                    total_students = students.count()

                    # Calculate percentage of attainment
                    if total_students > 0:
                        attainment_percentage = int((above_avg_count / total_students) * 100)
                    else:
                        attainment_percentage = 0

                    attainment_record, _ = AttainmentPercentage.objects.update_or_create(
                        passout_year=PassoutYear.objects.get(pk=selected_passout_year),
                        course=file_desc.course,
                        defaults={'attainment_percentage': attainment_percentage}
                    )
                    # Generate individual graph for the selected passout year and course
                    score_ranges = [i * 10 for i in range(11)]
                    score_counts = [students.filter(total_marks__range=(start, start + 9)).count() for start in score_ranges]
                    individual_graph = px.bar(x=score_ranges, y=score_counts, labels={'x': 'Score Range', 'y': 'Number of Students'})
                    individual_graph_html = individual_graph.to_html(full_html=False)

                    # Create DataFrame for trend graph data (across all passout years for the selected course)
                    trend_data = []
                    for passout_year in passout_years:
                        try:
                            year_file_desc = File_Description.objects.get(passout_year_id=passout_year.id, course_id=selected_course_id)
                            year_students = Student.objects.filter(file_desc=year_file_desc)
                            avg_marks = year_students.aggregate(avg_marks=Avg('total_marks'))['avg_marks']
                            if avg_marks is not None:
                                gte_avg_count = year_students.filter(total_marks__gte=avg_marks).count()
                                lt_avg_count = year_students.filter(total_marks__lt=avg_marks).count()
                                trend_data.append({'Passout Year': passout_year.year, 'Above Average': gte_avg_count, 'Below Average': lt_avg_count})
                        except File_Description.DoesNotExist:
                            pass

                    # Create DataFrame and generate trend graph
                    trend_df = pd.DataFrame(trend_data)
                    trend_graph = px.bar(trend_df, x='Passout Year', y=['Above Average', 'Below Average'],
                                         labels={'value': 'Count', 'variable': 'Category'},
                                         barmode='group', title='Passout Year-wise Comparison of Student Scores')
                    trend_graph_html = trend_graph.to_html(full_html=False)

                    return render(request, 'charts/visualize_scores.html', {
                        'passout_years': passout_years,
                        'courses': courses,
                        'selected_passout_year': selected_passout_year,
                        'year':PassoutYear.objects.get(pk=selected_passout_year).year,
                        'selected_course_id': selected_course_id,
                        'selected_course_name': selected_course_name,
                        'individual_graph_html': individual_graph_html,
                        'trend_graph_html': trend_graph_html,
                        'attainment_percentage': attainment_percentage
                    })

            except File_Description.DoesNotExist:
                pass

    # Default render for initial page load or invalid selection
    return render(request, 'charts/visualize_scores.html', {
        'passout_years': passout_years,
        'courses': courses,
        'selected_course_id': ''  # Default to no course selected
    })
