import pandas as pd
import plotly.express as px
from django.shortcuts import render, redirect
from django.db.models import Avg
from .models import *
from techapp.models import Course
import plotly.graph_objects as go
from django.http import HttpResponse, JsonResponse
from techapp.models import *



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



'''
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
                    gte_avg_count = students.filter(total_marks__gte=avg_total_marks).count()
                    total_students = students.count()

                    # Calculate percentage of attainment
                    if total_students > 0:
                        attainment_percentage = int((gte_avg_count / total_students) * 100)
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
                                trend_data.append({'Passout Year': passout_year.year, 'Average & Above Average': gte_avg_count, 'Below Average': lt_avg_count})
                        except File_Description.DoesNotExist:
                            pass

                    # Create DataFrame and generate trend graph
                    trend_df = pd.DataFrame(trend_data)
                    trend_graph = px.bar(trend_df, x='Passout Year', y=['Average & Above Average', 'Below Average'],
                                         labels={'value': 'Count', 'variable': 'Category'},
                                         barmode='group', title='Count of Average & Above Average ')
                    trend_graph_html = trend_graph.to_html(full_html=False)

                    context = {
                        'passout_years': passout_years,
                        'courses': courses,
                        'selected_passout_year': selected_passout_year,
                        'year':PassoutYear.objects.get(pk=selected_passout_year).year,
                        'selected_course_id': selected_course_id,
                        'selected_course_name': selected_course_name,
                        'individual_graph_html': individual_graph_html,
                        'trend_graph_html': trend_graph_html,
                        'attainment_percentage': attainment_percentage,
                        'gte_avg_count': gte_avg_count,
                        'total_students': total_students,
                    }
                    
                    return render(request, 'charts/visualize_scores.html', context)

            except File_Description.DoesNotExist:
                pass

    # Default render for initial page load or invalid selection
    return render(request, 'charts/visualize_scores.html', {
        'passout_years': passout_years,
        'courses': courses,
        'selected_course_id': ''  # Default to no course selected
    })'''


'''
import plotly.express as px
import pandas as pd
from django.shortcuts import render
from .models import PassoutYear, File_Description, Student

def visualize_course_trend(request):
    # Fetch distinct courses from File_Description
    courses = File_Description.objects.select_related('course').values_list('course__id', 'course__course_code').distinct()

    if request.method == 'GET':
        selected_course_id = request.GET.get('course_select')

        if selected_course_id:
            try:
                # Fetch all file descriptions for the selected course
                file_descs = File_Description.objects.filter(course_id=selected_course_id)

                # Prepare data for the trend graph
                trend_data = []

                # Define score ranges from 0 to 100 in intervals of 10
                score_ranges = list(range(0, 101, 10))

                # Iterate over each passout year and aggregate score counts
                for file_desc in file_descs:
                    passout_year = file_desc.passout_year.year
                    students = Student.objects.filter(file_desc=file_desc)

                    # Calculate count of students in each score range
                    score_counts = []
                    for i in range(len(score_ranges) - 1):
                        start = score_ranges[i]
                        end = score_ranges[i + 1]
                        count = students.filter(total_marks__gte=start, total_marks__lt=end).count()
                        score_counts.append(count)

                    # Append data for the passout year to trend_data
                    trend_data.append({'Passout Year': passout_year, **{f'Score Range {score_ranges[i]}-{score_ranges[i+1]-1}': count for i, count in enumerate(score_counts)}})

                # Create DataFrame for trend data
                trend_df = pd.DataFrame(trend_data)

                # Melt DataFrame to long format for plotting
                trend_df_melted = trend_df.melt(id_vars='Passout Year', var_name='Score Range', value_name='Count')

                # Create trend graph using Plotly Express
                trend_graph = px.line(trend_df_melted, x='Passout Year', y='Count', color='Score Range',
                                      labels={'Passout Year': 'Passout Year', 'Count': 'Number of Students', 'Score Range': 'Score Range'},
                                      title=f'Count of Students in Score Ranges (0-100) Across Years')

                # Convert graph to HTML for rendering in template
                trend_graph_html_1 = trend_graph.to_html(full_html=False)

                context = {
                    'courses': courses,
                    'selected_course_id': selected_course_id,
                    'trend_graph_html_1': trend_graph_html_1,
                }

                return render(request, 'charts/visualize_scores.html', context)

            except File_Description.DoesNotExist:
                pass

    # Default render for initial page load or invalid selection
    return render(request, 'charts/visualize_scores.html', {
        'courses': courses,
        'selected_course_id': ''  # Default to no course selected
    })
'''



# 4 gra[hs]


def visualization(request):
    # Fetch distinct passout years from File_Description
    passout_years = PassoutYear.objects.all()

    # Fetch distinct courses from File_Description
    courses = File_Description.objects.select_related('course').values_list('course__id', 'course__course_code').distinct()

    if request.method == 'GET':
        selected_passout_year = request.GET.get('passout_year_select')
        selected_course_id = request.GET.get('course_select')

        # Custom labels for score ranges
        score_labels = {        
                    ('O', 'S'): (90, 100),
                    ('A', 'A'): (80, 89),
                    ('A', 'B'): (70, 79),
                    ('B', 'B'): (60, 69),
                    ('B', 'C'): (50, 59),
                    ('C', 'C'): (40, 49),
                    ('C', 'D'): (30, 39),
                    ('D', 'D'): (20, 29),
                    ('E', 'E'): (10, 19),
                    ('F', 'F'): (0, 9)
                }
                

                # Map each student's score to the custom label
        scorecard = {}
        for label, (start, end) in score_labels.items():
            scorecard[f'{start}-{end}'] = label
        
        if selected_passout_year and selected_course_id:
            try:
                # Retrieve file description for the selected passout year and course
                file_desc = File_Description.objects.get(passout_year_id=selected_passout_year, course_id=selected_course_id)

                # Retrieve course name based on selected_course_id
                selected_course_name = file_desc.course.course_code

                # Retrieve students data for the selected passout year and course
                students = Student.objects.filter(file_desc=file_desc)

                # Calculate count of students in each score range (0-100 in intervals of 10)
                score_ranges = list(range(0, 101, 10))
                # Initialize score_counts list
                score_counts = []
                for start in score_ranges[:-1]:  # Iterate over score ranges
                    end = start + 10  # Calculate end of score range
                    count = students.filter(total_marks__range=(start, end-1)).count()  # Count students in range
                    score_counts.append(count)
                    
                    
                    
                # INdividual & Vs-graph
                avg_total_marks = students.aggregate(avg_total_marks=Avg('total_marks'))['avg_total_marks']
                if avg_total_marks is not None:
                    # Calculate counts of students scoring above and below average
                    gte_avg_count = students.filter(total_marks__gte=avg_total_marks).count()
                    total_students = students.count()

                    # Calculate percentage of attainment
                    if total_students > 0:
                        attainment_percentage = int((gte_avg_count / total_students) * 100)
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
                                trend_data.append({'Passout Year': passout_year.year, 'Average & Above Average': gte_avg_count, 'Below Average': lt_avg_count})
                        except File_Description.DoesNotExist:
                            pass

                    # Create DataFrame and generate trend graph
                    trend_df = pd.DataFrame(trend_data)
                    trend_graph = px.bar(trend_df, x='Passout Year', y=['Average & Above Average', 'Below Average'],
                                         labels={'value': 'Count', 'variable': 'Category'},
                                         barmode='group', title='Count of Average & Above Average ')
                    trend_graph_html = trend_graph.to_html(full_html=False)

                
                
                
                              
                # Create DataFrame for histogram data (across all passout years for the selected course)
                histogram_data = []
                for passout_year in passout_years:
                    try:
                        year_file_desc = File_Description.objects.get(passout_year_id=passout_year.id, course_id=selected_course_id)
                        year_students = Student.objects.filter(file_desc=year_file_desc)

                        # Calculate counts of students in each score range for the current passout year
                        score_counts_year = []
                        for start in score_ranges[:-1]:  # Iterate over score ranges
                            end = start + 10  # Calculate end of score range
                            count = year_students.filter(total_marks__range=(start, end-1)).count()  # Count students in range
                            score_counts_year.append(count)

                        histogram_data.append({'Passout Year': passout_year.year, **{f'Score Range {score_ranges[i]}-{score_ranges[i+1]-1}': count for i, count in enumerate(score_counts_year)}})

                    except File_Description.DoesNotExist:
                        pass

                # Create DataFrame for histograms
                histogram_df = pd.DataFrame(histogram_data)
                # Melt DataFrame to long format for plotting
                histogram_df_melted = histogram_df.melt(id_vars='Passout Year', var_name='Score Range', value_name='Count')

                # Create histogram using Plotly Express
                histogram_graph = px.bar(histogram_df_melted, x='Score Range', y='Count', color='Passout Year',
                                         barmode='group', labels={'Score Range': 'Score Range', 'Count': 'Number of Students', 'Passout Year': 'Passout Year'},
                                         title=f'Score Distribution Across Years for Course {selected_course_name}')

                histogram_graph_html = histogram_graph.to_html(full_html=False)
                
                
                
                
                # Line-graph              
                line_data = []
                for passout_year in passout_years:
                    try:
                        year_file_desc = File_Description.objects.get(passout_year_id=passout_year.id, course_id=selected_course_id)
                        year_students = Student.objects.filter(file_desc=year_file_desc)

                        # Calculate count of students in each score range for the current passout year
                        score_counts = [year_students.filter(total_marks__range=(start, start + 9)).count() for start in score_ranges]

                        # Append line graph data for the passout year
                        line_data.append({'Passout Year': passout_year.year, 'Score Counts': score_counts})

                    except File_Description.DoesNotExist:
                        pass

                # Create DataFrame for line graph data
                line_data = []
                for passout_year in passout_years:
                    try:
                        year_file_desc = File_Description.objects.get(passout_year_id=passout_year.id, course_id=selected_course_id)
                        year_students = Student.objects.filter(file_desc=year_file_desc)

                        # Calculate count of students in each score range for the current passout year
                        score_counts = [year_students.filter(total_marks__range=(start, start + 9)).count() for start in score_ranges]

                        # Append line graph data for the passout year
                        line_data.append({'Passout Year': passout_year.year, 'Score Counts': score_counts})

                    except File_Description.DoesNotExist:
                        pass

                # Create DataFrame for line graph data
                line_df = pd.DataFrame(line_data)

                # Prepare data for plotting line graph
                plot_data = []
                for index, row in line_df.iterrows():
                    passout_year = row['Passout Year']
                    for i, count in enumerate(row['Score Counts']):
                        plot_data.append({'Passout Year': passout_year, 'Score Range': f'{score_ranges[i]}-{score_ranges[i]+9}', 'Count of Students': count})

                # Create DataFrame for plotting
                plot_df = pd.DataFrame(plot_data)

                # Create line graph using Plotly Express with reversed axes
                line_graph = px.line(plot_df, x='Score Range', y='Count of Students', color='Passout Year',
                                     labels={'Score Range': 'Score Range', 'Count of Students': 'Number of Students', 'Passout Year': 'Passout Year'},
                                     title=f'Student Count in Score Ranges Across Years for Course {selected_course_name}')

                # Convert line graph to HTML for rendering in template
                line_graph_html = line_graph.to_html(full_html=False)

                
                
                # context = {
                #     'passout_years': passout_years,
                #     'courses': courses,
                #     'selected_passout_year': selected_passout_year,
                #     'year': PassoutYear.objects.get(pk=selected_passout_year).year,
                #     'selected_course_id': selected_course_id,
                #     'selected_course_name': selected_course_name,
                #     'histogram_graph_html': histogram_graph_html,
                #     'line_graph_html': line_graph_html,
                # }
                context = {
                    'passout_years': passout_years,
                    'courses': courses,
                    'selected_passout_year': selected_passout_year,
                    'year': PassoutYear.objects.get(pk=selected_passout_year).year,
                    'selected_course_id': selected_course_id,
                    'selected_course_name': selected_course_name,
                    'individual_graph_html': individual_graph_html,
                    'trend_graph_html': trend_graph_html,
                    'attainment_percentage': attainment_percentage,
                    'gte_avg_count': gte_avg_count,
                    'total_students': total_students,
                    'histogram_graph_html': histogram_graph_html,
                    'line_graph_html': line_graph_html,
                    'scorecard': scorecard  # Pass scorecard data to template
                }

                return render(request, 'charts/visualize_scores.html', context)

            except File_Description.DoesNotExist:
                pass

    # Default render for initial page load or invalid selection
    return render(request, 'charts/visualize_scores.html', {
        'passout_years': passout_years,
        'courses': courses,
        'selected_course_id': ''  # Default to no course selected
    })
'''


from django.shortcuts import render
from django.db.models import Avg
import pandas as pd
import plotly.express as px
from .models import PassoutYear, File_Description, Student

def visualization(request):
    # Fetch all passout years and distinct courses
    all_passout_years = PassoutYear.objects.all()
    distinct_courses = File_Description.objects.select_related('course').values_list('course__id', 'course__course_code').distinct()

    if request.method == 'GET':
        selected_passout_year = request.GET.get('passout_year_select')
        selected_course_id = request.GET.get('course_select')

        if selected_passout_year and selected_course_id:
            try:
                # Retrieve file description for the selected passout year and course
                file_description = File_Description.objects.get(passout_year_id=selected_passout_year, course_id=selected_course_id)

                # Retrieve course name based on selected course ID
                selected_course_name = file_description.course.course_code

                # Retrieve students data for the selected passout year and course
                students = Student.objects.filter(file_desc=file_description)

                # Calculate average total marks for all students
                average_total_marks = students.aggregate(avg_total_marks=Avg('total_marks'))['avg_total_marks']
                
                if average_total_marks is not None:
                    # Calculate counts of students scoring above and below average
                    above_avg_count = students.filter(total_marks__gte=average_total_marks).count()
                    below_avg_count = students.filter(total_marks__lt=average_total_marks).count()
                    total_students_count = students.count()

                    # Calculate attainment percentage
                    attainment_percentage = int((above_avg_count / total_students_count) * 100) if total_students_count > 0 else 0

                    # Generate histogram showing student count across score ranges for the selected passout year and course
                    score_ranges = list(range(0, 101, 10))
                    score_counts = [students.filter(total_marks__range=(start, start + 9)).count() for start in score_ranges]
                    histogram_graph = px.bar(x=score_ranges, y=score_counts, labels={'x': 'Score Range', 'y': 'Number of Students'})
                    histogram_graph_html = histogram_graph.to_html(full_html=False)

                    # Generate individual graph for the selected passout year and course
                    individual_graph = px.bar(x=score_ranges, y=score_counts, labels={'x': 'Score Range', 'y': 'Number of Students'})
                    individual_graph_html = individual_graph.to_html(full_html=False)

                    # Generate trend graph showing score range trends across passout years
                    trend_data = []
                    for year in all_passout_years:
                        year_students = Student.objects.filter(file_desc__passout_year=year, file_desc__course_id=selected_course_id)
                        year_score_counts = [year_students.filter(total_marks__range=(start, start + 9)).count() for start in score_ranges]
                        trend_data.append({'Passout Year': year.year, 'Score Counts': year_score_counts})

                    trend_df = pd.DataFrame(trend_data)
                    plot_data = []
                    for index, row in trend_df.iterrows():
                        passout_year = row['Passout Year']
                        for i, count in enumerate(row['Score Counts']):
                            plot_data.append({'Passout Year': passout_year, 'Score Range': f'{score_ranges[i]}-{score_ranges[i]+9}', 'Count of Students': count})

                    plot_df = pd.DataFrame(plot_data)
                    trend_graph = px.line(plot_df, x='Score Range', y='Count of Students', color='Passout Year')
                    trend_graph_html = trend_graph.to_html(full_html=False)

                    # Generate line graph showing student count in score ranges across years
                    line_graph = px.line(plot_df, x='Score Range', y='Count of Students', color='Passout Year')
                    line_graph_html = line_graph.to_html(full_html=False)

                    # Prepare context for rendering the template with named graph HTML
                    context = {
                        'all_passout_years': all_passout_years,
                        'distinct_courses': distinct_courses,
                        'selected_passout_year': selected_passout_year,
                        'selected_course_id': selected_course_id,
                        'selected_course_name': selected_course_name,
                        'attainment_percentage': attainment_percentage,
                        'histogram_graph_html': histogram_graph_html,
                        'individual_graph_html': individual_graph_html,
                        'trend_graph_html': trend_graph_html,
                        'line_graph_html': line_graph_html
                    }

                    return render(request, 'charts/visualize_scores.html', context)

            except File_Description.DoesNotExist:
                pass

    # Default render for initial page load or invalid selection
    return render(request, 'charts/visualize_scores.html', {
        'all_passout_years': all_passout_years,
        'distinct_courses': distinct_courses,
        'selected_course_id': ''  # Default to no course selected
    })
'''