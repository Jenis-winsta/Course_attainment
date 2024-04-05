# views.py
import pandas as pd
<<<<<<< HEAD
from django.shortcuts import render, redirect
from .forms import ExcelUploadForm
from .models import Student, File_Description
import plotly.graph_objects as go
from django.db.models import Avg


def handle_excel_file(file, year, sheet_name):
    # Load Excel file into pandas DataFrame
    xls = pd.ExcelFile(file)

    # Iterate through each sheet in the Excel file
    for sheet_name in xls.sheet_names:
        # Read data from the sheet
        df = pd.read_excel(xls, sheet_name)
        
        # Check if df is a DataFrame and contains data
        if isinstance(df, pd.DataFrame) and not df.empty:
            # Rename the first four headers
            df.columns = ['name', 'cia_marks', 'semester_marks', 'total_marks'] + list(df.columns[4:])
            
            # Create File_Description object with sheet_name if available
            if sheet_name:
                file_desc = File_Description.objects.create(year=year, sheet_name=sheet_name)
            else:
                file_desc = File_Description.objects.create(year=year)
            
            # Process and save data to the database
            process_data(df, file_desc)
        else:
            # Log or raise an error if the DataFrame is empty or not in the expected format
            print(f"DataFrame for sheet '{sheet_name}' is empty or not in the expected format.")
=======
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

>>>>>>> error

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

<<<<<<< HEAD
def visualize_scores(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            year = request.POST.get('year')
            sheet_name = request.POST.get('sheet_name')
            handle_excel_file(file, year, sheet_name)
            return redirect('visualization_page')
    else:
        form = ExcelUploadForm()
=======
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
>>>>>>> error

    return render(request, 'charts/upload_form.html', {'form': form})

<<<<<<< HEAD
def visualization_page(request):
    years = File_Description.objects.values_list('year', flat=True).distinct()

    individual_graphs = {}
    trend_graphs = {}

    if request.method == 'POST':
        selected_year = request.POST.get('year')
        selected_sheet_name = request.POST.get('sheet_name')

        if selected_year is not None:
            file_desc = File_Description.objects.get(year=selected_year, sheet_name=selected_sheet_name)

            students = Student.objects.filter(file_desc=file_desc)

            # Generate individual graph for the selected year and sheet
            score_ranges = [i * 10 for i in range(11)]
            score_counts = [students.filter(total_marks__range=(start, start + 9)).count() for start in score_ranges]
            individual_graph = go.Figure(data=[go.Bar(x=score_ranges, y=score_counts)])
            individual_graph.update_layout(title=f'Student Scores for {file_desc}', xaxis=dict(title='Score Range'), yaxis=dict(title='Number of Students'))
            individual_graphs[file_desc.sheet_name] = individual_graph.to_html(full_html=False)

            # Compare data year-wise for the selected sheet
            gte_avg_counts = []
            lt_avg_counts = []

            for year in years:
                year_file_desc = File_Description.objects.get(year=year, sheet_name=selected_sheet_name)
                year_students = Student.objects.filter(file_desc=year_file_desc)
                avg_total_marks = year_students.aggregate(avg_total_marks=Avg('total_marks'))['avg_total_marks']
                gte_avg_count = year_students.filter(total_marks__gte=avg_total_marks).count()
                lt_avg_count = year_students.filter(total_marks__lt=avg_total_marks).count()
                gte_avg_counts.append(gte_avg_count)
                lt_avg_counts.append(lt_avg_count)

            # Generate trend graph for the selected sheet
            x_labels = [str(year) for year in years]
            trace1 = go.Bar(x=x_labels, y=lt_avg_counts, name='Less than Average')
            trace2 = go.Bar(x=x_labels, y=gte_avg_counts, name='Greater than or equal to Average')
            trend_graph = go.Figure(data=[trace1, trace2])
            trend_graph.update_layout(title=f'Year-wise Comparison of Student Scores - {selected_sheet_name}', xaxis=dict(title='Year'), yaxis=dict(title='Count'), width=800)
            trend_graphs[selected_sheet_name] = trend_graph.to_html(full_html=False)

    return render(request, 'charts/visualize_scores.html', {'years': years, 'individual_graphs': individual_graphs, 'trend_graphs': trend_graphs})


'''
def handle_excel_file(file):
    # Load Excel file into pandas DataFrame
    xls = pd.ExcelFile(file)
    sheet_names = xls.sheet_names

    for sheet_name in sheet_names:
        # Read data from each sheet
        df = pd.read_excel(xls, sheet_name)

        # Rename the first four headers
        df.columns = ['Student', 'CIA', 'End Sem', 'Total'] + list(df.columns[4:])

        # Skip empty rows at the beginning
        df = df.dropna(axis=0, how='all')

        # Process data and save to database
        process_data(df)

def process_data(df):
    # Your data processing logic here
    # For example, iterating through DataFrame rows and saving to database
    for index, row in df.iterrows():
        # Example: Creating Student objects and saving to database
        student = Student.objects.create(
            name=row['Student'],
            cia_marks=row['CIA'],
            semester_marks=row['End Sem'],
            total_marks=row['Total']
        )

def visualize_scores(request):
    # Get distinct years from the database
    years = File_Description.objects.values_list('year', flat=True).distinct()

    individual_graph_html = None
    trend_graph_html = None

    if request.method == 'POST':
        selected_year = request.POST.get('year')

        if selected_year is not None:  # Check if selected_year is not None
            # Generate graph for the selected year
            students = Student.objects.filter(file_desc__year=selected_year)
            average_marks = students.aggregate(avg_total_marks=models.Avg('total_marks'))['avg_total_marks']

            # Count of students in each score range (frequency of 10 marks)
            score_ranges = [i * 10 for i in range(11)]
            score_counts = [students.filter(total_marks__range=(start, start + 9)).count() for start in score_ranges]

            # Create Plotly bar graph for individual year
            individual_graph = go.Figure(data=[go.Bar(x=score_ranges, y=score_counts)])
            individual_graph.update_layout(title=f'Student Scores for {selected_year}',
                                           xaxis=dict(title='Score Range'), yaxis=dict(title='Number of Students'))

            individual_graph_html = individual_graph.to_html(full_html=False)

            # Compare all data year-wise
            if request.POST.get('compare_all'):
                # Lists to store data for comparison graph
                gte_avg_counts = []
                lt_avg_counts = []
                years_with_data = []

                # Filter years with data and populate lists
                for year in years:
                    students = Student.objects.filter(file_desc__year=year)
                    if students.exists():
                        years_with_data.append(year)
                        average_marks = students.aggregate(avg_total_marks=models.Avg('total_marks'))['avg_total_marks']
                        gte_avg_count = students.filter(total_marks__gte=average_marks).count()
                        lt_avg_count = students.filter(total_marks__lt=average_marks).count()
                        gte_avg_counts.append(gte_avg_count)
                        lt_avg_counts.append(lt_avg_count)

                if years_with_data:
                    # Create Plotly bar graph for trend comparison
                    x_labels = [str(year) for year in years_with_data]
                    trace1 = go.Bar(x=x_labels, y=lt_avg_counts, name='Less than Average')
                    trace2 = go.Bar(x=x_labels, y=gte_avg_counts, name='Greater than or equal to Average')

                    trend_graph = go.Figure(data=[trace1, trace2])
                    trend_graph.update_layout(title='Year-wise Comparison of Student Scores',
                                              xaxis=dict(title='Year'), yaxis=dict(title='Count'),
                                              width=800)  # Adjust width here

                    trend_graph_html = trend_graph.to_html(full_html=False)
                else:
                    trend_graph_html = "<p>No data available for comparison.</p>"

    return render(request, 'charts/visualize_scores.html', {'years': years, 'individual_graph': individual_graph_html, 'trend_graph': trend_graph_html})


def import_excel(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['file']
            year = form.cleaned_data['year']
            try:
                df = pd.read_excel(excel_file)
                for index, row in df.iterrows():
                    Student.objects.create(
                        name=row['Student'],
                        cia_marks=row['CIA'],
                        semester_marks=row['End Sem'],
                        total_marks=row['Total'],
                        file_desc_id=year.id,                        

                        # year=year
                    )
                messages.success(request, 'Excel file imported successfully.')
                return redirect('import_excel')
            except IndexError:
                pass
        else:
            messages.error(request, 'Invalid form submission.')
    else:
        form = ExcelUploadForm()
    
    # passing variables  to the template using dictionary
    context= {
        'form': form,
    }
    
    return render(request, 'charts/import_excel.html', context)
=======
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

>>>>>>> error
'''


def visualization_page(request):
    years = File_Description.objects.values_list('year', flat=True).distinct()

    individual_graphs = {}
    trend_graphs = {}

<<<<<<< HEAD
=======
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
>>>>>>> error

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

<<<<<<< HEAD
# # plotting using plotly express
# # views.py

# def visualize_scores(request):
#     # Get distinct years from the database
#     years = File_Description.objects.values_list('year', flat=True).distinct()

#     individual_graph_html = None
#     trend_graph_html = None

#     if request.method == 'POST':
#         selected_year = request.POST.get('year')

#         if selected_year is not None:  # Check if selected_year is not None
#             # Generate graph for the selected year
#             students = Student.objects.filter(file_desc__year=selected_year)
#             average_marks = students.aggregate(avg_total_marks=models.Avg('total_marks'))['avg_total_marks']

#             # Count of students in each score range (frequency of 10 marks)
#             score_ranges = [i * 10 for i in range(11)]
#             score_counts = [students.filter(total_marks__range=(start, start + 9)).count() for start in score_ranges]

#             # Create Plotly bar graph for individual year
#             individual_graph = go.Figure(data=[go.Bar(x=score_ranges, y=score_counts)])
#             individual_graph.update_layout(title=f'Student Scores for {selected_year}',
#                                            xaxis=dict(title='Score Range'), yaxis=dict(title='Number of Students'))

#             individual_graph_html = individual_graph.to_html(full_html=False)

#             # Compare all data year-wise
#             if request.POST.get('compare_all'):
#                 # Lists to store data for comparison graph
#                 gte_avg_counts = []
#                 lt_avg_counts = []
#                 years_with_data = []

#                 # Filter years with data and populate lists
#                 for year in years:
#                     students = Student.objects.filter(file_desc__year=year)
#                     if students.exists():
#                         years_with_data.append(year)
#                         average_marks = students.aggregate(avg_total_marks=models.Avg('total_marks'))['avg_total_marks']
#                         gte_avg_count = students.filter(total_marks__gte=average_marks).count()
#                         lt_avg_count = students.filter(total_marks__lt=average_marks).count()
#                         gte_avg_counts.append(gte_avg_count)
#                         lt_avg_counts.append(lt_avg_count)

#                 if years_with_data:
#                     # Create Plotly bar graph for trend comparison
#                     x_labels = [str(year) for year in years_with_data]
#                     trace1 = go.Bar(x=x_labels, y=lt_avg_counts, name='Less than Average')
#                     trace2 = go.Bar(x=x_labels, y=gte_avg_counts, name='Greater than or equal to Average')

#                     trend_graph = go.Figure(data=[trace1, trace2])
#                     trend_graph.update_layout(title='Year-wise Comparison of Student Scores',
#                                               xaxis=dict(title='Year'), yaxis=dict(title='Count'),
#                                               width=800)  # Adjust width here

#                     trend_graph_html = trend_graph.to_html(full_html=False)
#                 else:
#                     trend_graph_html = "<p>No data available for comparison.</p>"

#     return render(request, 'charts/visualize_scores.html', {'years': years, 'individual_graph': individual_graph_html, 'trend_graph': trend_graph_html})
=======
    return render(request, 'charts/visualize_scores.html', {'years': years, 'individual_graphs': individual_graphs, 'trend_graphs': trend_graphs})
>>>>>>> error
