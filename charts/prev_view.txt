from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage 
import plotly
from tablib import Dataset
import plotly.graph_objs as go
import plotly.express as px

from charts import models
from .resources import StudentResource
from .models import Student
from .forms import UploadFileForm
from django.db.models import Avg
from .utils import process_excel_file



def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            new_file = request.FILES['file']
            if not new_file.name.endswith('.xlsx'):
                messages.error(request, 'Please upload a valid Excel file with a .xlsx extension.')
                return redirect('upload_file')
            
            try:
                process_excel_file(new_file)
                messages.success(request, 'Data imported successfully.')
            except IndexError:
                pass
            
            return redirect('upload_file')
    else:
        form = UploadFileForm()
    
    return render(request, 'charts/upload.html', {'form': form})



'''
# Excel file upload
def upload_file(request):
    if request.method == 'POST':
        student_resource = StudentResource()
        dataset = Dataset()
        
        new_files = request.FILES['file']                    
        
        if not new_files.name.endswith('xlsx'):
            messages.error(request, 'Please upload a valid Excel file which ends with ".xlsx"')
            return redirect('upload_file')
        
        # using functionality in utils file    
        process_excel_file(new_files)
        
        imported_data = dataset.load(new_files.read(), format='xlsx')
        for data in imported_data[1:]:
            try:
                student = Student(
                    name=data[0],
                    cia_marks=data[1],
                    sem_marks=data[2],
                    total_marks=data[3],
                )
                student.save()
            except IndexError:
                pass
        
        messages.success(request, 'Data imported Successfully.')
        return redirect('upload_file')
    else:
        return render(request, 'charts/upload.html', {'form': UploadFileForm()})
'''



def visualize_marks(request):
    # Get unique sheet names
    sheet_names = Student.objects.values_list('file_name', flat=True).distinct()

    # Initialize lists to store data for the combined graph
    x_data = []
    y_data = []
    sheet_labels = []

    # Calculate average marks for each sheet
    for sheet_name in sheet_names:
        students = Student.objects.filter(file_name=sheet_name)
        average_marks = students.aggregate(avg_total_marks=Avg('total_marks'))['avg_total_marks']

        # Filter students scoring more than average marks
        students_above_average = students.filter(total_marks__gt=average_marks)
        student_names = [student.name for student in students_above_average]
        marks_above_average = [student.total_marks for student in students_above_average]

        # Append data to lists
        x_data.extend(student_names)
        y_data.extend(marks_above_average)
        sheet_labels.extend([sheet_name] * len(student_names))

    # Create the combined graph
    fig = go.Figure()
    for sheet_name in sheet_names:
        mask = [label == sheet_name for label in sheet_labels]
        fig.add_trace(go.Bar(x=[x_data[i] for i in range(len(x_data)) if mask[i]], 
                             y=[y_data[i] for i in range(len(y_data)) if mask[i]], 
                             name=sheet_name))

    fig.update_layout(title='Students Scoring More than Average Marks (Sheet-wise)',
                      xaxis_title='Student Name',
                      yaxis_title='Marks',
                      barmode='group')  # Adjust barmode as per your preference (e.g., 'group', 'stack')

    # Convert plot to HTML
    combined_graph_html = fig.to_html(full_html=False, include_plotlyjs='cdn')

    context = {
        'combined_graph_html': combined_graph_html,
    }

    return render(request, 'charts/visualization.html', context)


'''

# Visualizing using Plotly
def visualize_marks(request):
    students = Student.objects.all()  
    # students = Student.objects.filter(file_name=file_name)  
    
    average_marks = int(students.aggregate(avg_total_marks=Avg('total_marks'))['avg_total_marks'])    
    
    student_names = [student.name for student in students if student.total_marks > average_marks]    
    marks_above_average = [student.total_marks for student in students if student.total_marks > average_marks]
    # markiee = [student.total_marks for student in students if student.total_marks > average_marks]
    total_students = students.count()
    
    above_average_count = len(marks_above_average)
    probability_above_average = (above_average_count / total_students) * 100
    
    
    
    # Plot histogram
    fig = go.Figure()    
    # Add histogram trace
    fig.add_trace(go.Histogram(x=marks_above_average, histnorm='probability', name='Marks Distribution', hoverinfo='x+y+name', hovertemplate='Total Marks: %{x}<br>Probability: %{y:.2f}<extra>Above Average</extra>'), )    
    # Update layout
    fig.update_layout(title='Distribution of Marks Above Average', xaxis_title='Total Marks', yaxis_title='Probability',  showlegend=True)    
    # Convert plot to HTML
    graph_html = fig.to_html(full_html=False, default_height=500, default_width=700)
    
    
    # marks less than equal to average
    marks_lte_average = [student.total_marks for student in students if student.total_marks <= average_marks]
    lte_average_count = len(marks_lte_average)
    probability_lte_average = (lte_average_count / total_students) * 100
    # lte avg
    fig1 = go.Figure()
    fig1.add_trace(go.Histogram(x=marks_lte_average, histnorm='probability', name='Marks Distribution', hoverinfo='x+y+name', hovertemplate='Total Marks: %{x}<br>Probability: %{y:.2f}<extra>Less than Equal to Average</extra>'))
    fig1.update_layout(title='Distribution of Marks Less than Equal to Average', xaxis_title='Total Marks', yaxis_title='Probability',  showlegend=True)
    graph_html_1 = fig1.to_html(full_html=False, default_height=500, default_width=700)
    
    
    # gt target
    marks_gt_target = [student.total_marks for student in students if student.total_marks > 60]
    gt_target_count = len(marks_gt_target)
    probability_gt_target = (gt_target_count / total_students) * 100
    # gt target
    fig2 = go.Figure()
    fig2.add_trace(go.Histogram(x=marks_gt_target, histnorm='probability', name='Marks Distribution', hoverinfo='x+y+name', hovertemplate='Total Marks: %{x}<br>Probability: %{y:.2f}<extra>Greater than Target</extra>'))
    fig2.update_layout(title='Distribution of Marks Greater than Target', xaxis_title='Total Marks', yaxis_title='Probability',  showlegend=True)
    graph_html_2 = fig2.to_html(full_html=False, default_height=500, default_width=700)
    
    
    
    summary_report = f"Out of {total_students} students, {above_average_count} students ({probability_above_average:.2f}%) scored above the average marks of {average_marks:.2f}."
    summary_report_1 = f"Out of {total_students} students, {lte_average_count} students ({probability_lte_average:.2f}%) scored less than equal to the average marks of {average_marks:.2f}."
    summary_report_2 = f"Out of {total_students} students, {gt_target_count} students ({probability_gt_target:.2f}%) scored above the target set: 60%"
    
    context = {
        'average_marks': average_marks,        
        'summary_report': summary_report,
        'graph_html': graph_html,
        
        
        'summary_report_1': summary_report_1,        
        'graph_html_1': graph_html_1,
                
        
        'summary_report_2': summary_report_2,        
        'graph_html_2': graph_html_2,
        
    }
    return render(request, 'charts/visualization.html', context)


'''




# def marks_gt_60(request):
    
#     students = Student.objects.all()    
    
#     # average_marks = students.aggregate(avg_total_marks=Avg('total_marks'))['avg_total_marks']
#     student_names = [student.name for student in students if student.total_marks > 60]    
#     marks_above_60 = [student.total_marks for student in students if student.total_marks > 60]
    
#     total_students = students.count()
#     above_60_count = len(marks_above_60)
#     probability_above_60 = (above_60_count / total_students) * 100
    
#     # Plot histogram
#     fig = go.Figure()
    
#     # Add histogram trace
#     fig.add_trace(go.Histogram(x=marks_above_60, histnorm='probability', name='Marks Distribution', hoverinfo='x+y+name', hovertemplate='Total Marks: %{x}<br>Probability: %{y:.2f}<extra>Above 60</extra>'))
    
#     # Update layout
#     fig.update_layout(title='Distribution of Marks Above 60', xaxis_title='Total Marks', yaxis_title='Probability', showlegend=True)
    
#     # Convert plot to HTML
#     graph_html_gt_60 = fig.to_html(full_html=False, default_height=500, default_width=700)
    
#     summary_report = f"Out of {total_students} students, {above_60_count} students ({probability_above_60:.2f}%) scored above 60 marks."
    
#     context = {
#         'summary_report': summary_report,
#         'graph_html_gt_60': graph_html_gt_60,
#     }
    
#     return render(request, 'charts/60.html', context)

# def marks_gt_80(request):
    
#     students = Student.objects.all()    
    
#     # average_marks = students.aggregate(avg_total_marks=Avg('total_marks'))['avg_total_marks']
#     student_names = [student.name for student in students if student.total_marks > 80]    
#     marks_above_80 = [student.total_marks for student in students if student.total_marks > 80]
    
#     total_students = students.count()
#     above_80_count = len(marks_above_80)
#     probability_above_80 = (above_80_count / total_students) * 100
    
#     # Plot histogram
#     fig = go.Figure()
    
#     # Add histogram trace
#     fig.add_trace(go.Histogram(x=marks_above_80, histnorm='probability', name='Marks Distribution', hoverinfo='x+y+name', hovertemplate='Total Marks: %{x}<br>Probability: %{y:.2f}<extra>Above 80</extra>'))
    
#     # Update layout
#     fig.update_layout(title='Distribution of Marks Above 80', xaxis_title='Total Marks', yaxis_title='Probability', showlegend=True)
    
#     # Convert plot to HTML
#     graph_html_gt_80 = fig.to_html(full_html=False, default_height=500, default_width=700)
    
#     summary_report = f"Out of {total_students} students, {above_80_count} students ({probability_above_80:.2f}%) scored above 80 marks."
    
#     context = {
#         'summary_report': summary_report,
#         'graph_html_gt_80': graph_html_gt_80,
#     }
    
#     return render(request, 'charts/80.html', context)


# def dum(request):
#     students = Student.objects.all()
#     average_marks = students.aggregate(avg_total_marks=Avg('total_marks'))['avg_total_marks']
#     students_above_average = [student for student in students if student.total_marks > average_marks]
#     return render(request, 'charts/dum.html', {'students_above_average': students_above_average, 'average_marks': average_marks})

#     # return render(request, 'charts/dum.html')




















# # def simple_upload(request):
# #     if request.method == 'POST':
# #         student_resource = StudentResource()
# #         dataset = Dataset()
# #         new_file = request.FILES.get('file')
        
# #         if not new_file or not new_file.name.endswith('xlsx'):
# #             mes`sa`ges.error(request, 'Please upload a valid Excel file.')
# #             return render(request, 'upload.html')
        
        
# #         imported_data = dataset.load(new_file.read(), format='xlsx')

# #         for data in imported_data[1:]:        
# #             try:
# #                 Student.objects.create(
# #                     name=data[1],
# #                     cia_marks=data[2],
# #                     sem_marks=data[3],
# #                     total_marks=data[4],
# #                 )
# #             except IndexError:
# #                 messages.error(request, 'Invalid data format.')
# #                 return redirect('upload_excel')

# #             messages.success(request, 'Data imported successfully.')
# #             return redirect('upload_excel')  # Redirect to the upload page after successful upload

# #     return render(request, 'charts/upload.html')
