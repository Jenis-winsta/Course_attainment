from django.shortcuts import render
from django.contrib import messages
from .resources import DataResource
from tablib import Dataset
from .models import Data

def simple_upload(request):
    if request.method == 'POST':
        data_resource = DataResource()
        dataset = Dataset()
        new_data = request.FILES['myFile']

        if not new_data.name.endswith('xlsx'):
            messages.error(request, 'Wrong format')
            return render(request, 'upload.html')

        imported_data = dataset.load(new_data.read(), format='xlsx')
        
        # Skip the first row (headers) and iterate over the rest
        for data in imported_data[1:]:
            try:
                value = Data.objects.create(
                    name=data[1],
                    cia_marks=data[2],
                    ese_marks=data[3],
                    total_marks=data[4],
                )
                value.save()
            except IndexError:
                # Handle any index errors gracefully
                pass

    return render(request, 'upload.html') 