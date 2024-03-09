from django.shortcuts import render, redirect
from django.contrib import messages
from .resources import StudentResource
from tablib import Dataset
from .models import Student

def simple_upload(request):
    if request.method == 'POST':
        student_resource = StudentResource()
        new_student = request.FILES.get('myfile')
        
        if not new_student or not new_student.name.endswith('xlsx'):
            messages.error(request, 'Please upload a valid Excel file.')
            return redirect('upload_excel')
        
        dataset = Dataset()
        imported_data = dataset.load(new_student.read(), format='xlsx')

        try:
            for data in imported_data[1:]:
                Student.objects.create(
                    name=data[1],
                    cia_marks=data[2],
                    sem_marks=data[3],
                    total_marks=data[4],
                )
        except IndexError:
            messages.error(request, 'Invalid data format.')
            return redirect('upload_excel')

        messages.success(request, 'Data imported successfully.')
        return redirect('upload_excel')  # Redirect to the upload page after successful upload

    return render(request, 'charts/upload.html')
