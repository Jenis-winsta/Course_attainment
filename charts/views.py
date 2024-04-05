# views.py
import pandas as pd
import plotly.express as px
from django.shortcuts import render, redirect
from django.http import HttpResponse
# from .forms import UploadForm
from .models import *
from django.db.models import Avg
from techapp.models import *

from django.http import HttpResponseRedirect
from django.urls import reverse


import pandas as pd
from django.shortcuts import render, redirect


def handle_excel_file(file, year_of_file, course_code):
    # Load Excel file into Pandas DataFrame
    df = pd.read_excel(file)

    course = Course.objects.get(course_code=course_code)
    # Create File_Description object
    file_desc = File_Description.objects.get(year_of_file=year_of_file, course=course)
    
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

# def upload_data(request):
#     if request.method == 'POST':
#         year = request.POST.get('year_of_file')
#         print(year)
#         form = UploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             file = form.cleaned_data['file']
#             year_of_file = form.cleaned_data['year_of_file']
#             course_code = form.cleaned_data['course_code']
#             handle_excel_file(file, year_of_file, course_code)
#             return redirect('visualization_page')
#         else:
#             print("Form is invalid: ", form.errors)
#     else:
#         form = UploadForm()

#     years = File_Description.objects.values_list('year_of_file', flat=True).distinct()
#     course_codes = File_Description.objects.values_list('course__course_code', flat=True).distinct()

#     return render(request, 'charts/upload_form.html', {'form': form, 'years': years, 'course_codes': course_codes})
from django.shortcuts import render



def upload_data(request):
    years =  File_Description.objects.values_list('year_of_file', flat=True).distinct()
    course_codes = File_Description.objects.values_list('course__course_code', flat=True).distinct()

    context={
        'years': years, 
        'course_codes': course_codes
    }
    return render(request, 'charts/upload_form.html', context)








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



def visualization(request):
    years = File_Description.objects.values_list('year_of_file', flat=True).distinct()

    individual_graphs = {}
    trend_graphs = {}

    if request.method == 'POST':
        file = request.FILES['file']
        
        # You can access other form data like this:
        year_of_file = request.POST.get('year_of_file')
        course_code = request.POST.get('course_code')

        # Assuming the uploaded file is in Excel format
        if file.name.endswith('.xlsx') or file.name.endswith('.xls'):
            # print("hello")
            df = pd.read_excel(file)
            handle_excel_file(file, year_of_file, course_code)

        # print("reached post of visualization")
        selected_year = request.POST.get('year_of_file')
        selected_course_code = request.POST.get('course_code')
        # print(selected_course_code)
        # print(selected_year)

        if selected_year is not None and selected_course_code is not None:
            course = Course.objects.get(course_code=selected_course_code)
            # Create File_Description object
            file_desc = File_Description.objects.get(year_of_file=selected_year, course=course)
            
            # file_desc = File_Description.objects.get(year_of_file=selected_year, course_code=selected_course_code)

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

            

            # Inside the loop where you're calculating average total marks
            for year in years:
                year_file_desc = File_Description.objects.get(year_of_file=year, course=course)
                year_students = Student.objects.filter(file_desc=year_file_desc)
                avg_total_marks = year_students.aggregate(avg_total_marks=Avg('total_marks'))['avg_total_marks']
                if avg_total_marks is not None:
                    gte_avg_count = year_students.filter(total_marks__gte=avg_total_marks).count()
                    lt_avg_count = year_students.filter(total_marks__lt=avg_total_marks).count()
                    gte_avg_counts.append(gte_avg_count)
                    lt_avg_counts.append(lt_avg_count)
                else:
                    # Handle case where no students exist for the year
                    gte_avg_counts.append(0)
                    lt_avg_counts.append(0)


            # Generate trend graph
            trend_graph = px.bar(x=[str(year) for year in years], y=[lt_avg_counts, gte_avg_counts], labels={'x': 'Year', 'y': 'Count'}, width=800)
            trend_graph.update_layout(title='Year-wise Comparison of Student Scores', xaxis_title='Year', yaxis_title='Count')
            trend_graphs[selected_year] = trend_graph.to_html(full_html=False)

    return render(request, 'charts/visualize_scores.html', {'years': years, 'individual_graphs': individual_graphs, 'trend_graphs': trend_graphs})
