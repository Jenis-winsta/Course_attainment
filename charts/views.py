# views.py
import pandas as pd
import plotly.express as px
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UploadForm
from .models import Student, File_Description
from django.db.models import Avg
from techapp.models import *


import pandas as pd
from django.shortcuts import render, redirect
from .forms import UploadForm
from .models import File_Description, Student

def handle_excel_file(file, year_of_file, course_code):
    # Load Excel file into Pandas DataFrame
    df = pd.read_excel(file)

    # Create File_Description object
    file_desc = File_Description.objects.create(year_of_file=year_of_file, course__course_code=course_code)
    
    # Rename the first four headers
    df.columns = ['name', 'cia_marks', 'semester_marks', 'total_marks'] + list(df.columns[4:])
    
    # Process and save data to the database
    process_data(df, file_desc)


def process_data(df, file_desc):
    # Iterate through DataFrame rows and save to database
    for index, row in df.iterrows():
        Student.objects.create(
            name=row['name'],
            cia_marks=row['cia_marks'],
            semester_marks=row['semester_marks'],
            total_marks=row['total_marks'],
            file_desc=file_desc
        )

def upload_data(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            year_of_file = form.cleaned_data['year_of_file']
            course_code = form.cleaned_data['course_code']
            handle_excel_file(file, year_of_file, course_code)
            return redirect('visualization_page')
        else:
            print("Form is invalid: ", form.errors)
    else:
        form = UploadForm()

    years = File_Description.objects.values_list('year_of_file', flat=True).distinct()
    course_codes = File_Description.objects.values_list('course__course_code', flat=True).distinct()

    return render(request, 'charts/upload_form.html', {'form': form, 'years': years, 'course_codes': course_codes})





# def handle_excel_file(file, year_of_file, course_code):
# # def handle_excel_file(file, year_of_file):

#     # Load Excel file into Pandas DataFrame
#     df = pd.read_excel(file)
#     # Create File_Description object
#     file_desc = File_Description.objects.create(year_of_file=year_of_file, course__course_code=course_code)  
#     # file_desc = File_Description.objects.create(year_of_file=year_of_file)  
    
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
#     if request.method == 'POST':
#         form = UploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             # files = request.FILES['file']
#             file = form.cleaned_data['file']
#             year_of_file = form.cleaned_data['year_of_file']
#             course_code = form.cleaned_data['course_code']
#             handle_excel_file(file, year_of_file, course_code)
#             handle_excel_file(file, year_of_file)
            
#             return redirect('visualization_page')
#         else:
#             print("Form is invalid: ", form.errors)
#     else:
#         form = UploadForm()

#     years = File_Description.objects.values_list('year_of_file', flat=True).distinct()
#     course_codes = File_Description.objects.values_list('course__course_code', flat=True).distinct()

#     return render(request, 'charts/upload_form.html', {'form': form, 'years': years, 'course_codes': course_codes})    #
'''


def upload_data(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            # year = form.cleaned_data['year']
            # course_code = form.cleaned_data['course_code']
            
            # No need to create a new form here
            # form = UploadForm()
            
            # print("Year: ",year)
            print("File: ",file.name)
            print("Data saved success")
        
            # handle_excel_file(file, year, course_code)
            handle_excel_file(file)
            
            return redirect('visualization_page')
        else:
            print("Form is invalid:", form.errors)
    else:
        form = UploadForm()
        
    # years = File_Description.objects.values_list('year', flat=True).distinct()
    # course_codes = Course.objects.values_list('course_code', flat=True).distinct()

    # return render(request, 'charts/upload_form.html', {'form': form, 'years': years, 'course_codes': course_codes})
    return render(request, 'charts/upload_form.html', {'form': form})

'''


def visualization_page(request):
    years = File_Description.objects.values_list('year', flat=True).distinct()

    individual_graphs = {}
    trend_graphs = {}

    if request.method == 'POST':
        selected_year = request.POST.get('year')
        selected_course_code = request.POST.get('course_code')

        if selected_year is not None and selected_course_code is not None:
            file_desc = File_Description.objects.get(year=selected_year, course_code=selected_course_code)

            students = Student.objects.filter(file_desc=file_desc)

            # Generate individual graph for the selected year
            score_ranges = [i * 10 for i in range(11)]
            score_counts = [students.filter(total_marks__range=(start, start + 9)).count() for start in score_ranges]
            individual_graph = px.bar(x=score_ranges, y=score_counts, labels={'x': 'Score Range', 'y': 'Number of Students'})
            individual_graph.update_layout(title=f'Student Scores for {selected_year}', xaxis_title='Score Range', yaxis_title='Number of Students')
            individual_graphs[selected_year] = individual_graph.to_html(full_html=False)

            # Compare data year-wise
            gte_avg_counts = []
            lt_avg_counts = []

            for year in years:
                year_file_desc = File_Description.objects.get(year=year, course_code=selected_course_code)
                year_students = Student.objects.filter(file_desc=year_file_desc)
                avg_total_marks = year_students.aggregate(avg_total_marks=pd.NamedAgg(column='total_marks', aggfunc='mean'))['avg_total_marks']
                gte_avg_count = year_students.filter(total_marks__gte=avg_total_marks).count()
                lt_avg_count = year_students.filter(total_marks__lt=avg_total_marks).count()
                gte_avg_counts.append(gte_avg_count)
                lt_avg_counts.append(lt_avg_count)

            # Generate trend graph
            trend_graph = px.bar(x=[str(year) for year in years], y=[lt_avg_counts, gte_avg_counts], labels={'x': 'Year', 'y': 'Count'}, width=800)
            trend_graph.update_layout(title='Year-wise Comparison of Student Scores', xaxis_title='Year', yaxis_title='Count')
            trend_graphs[selected_year] = trend_graph.to_html(full_html=False)

    return render(request, 'charts/visualize_scores.html', {'years': years, 'individual_graphs': individual_graphs, 'trend_graphs': trend_graphs})
