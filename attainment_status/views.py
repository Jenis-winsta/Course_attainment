# from django.shortcuts import render

# # Create your views here.
# from django.shortcuts import render
# import openpyxl
# from openpyxl import load_workbook
# from .models import Product

# def import_from_excel(request):
#     if request.method == 'POST':
#         excel_file = request.FILES['excel_file']
#         wb = load_workbook(excel_file)
#         ws = wb.active

#         for row in ws.iter_rows(min_row=2, values_only=True):
#             name, price, quantity = row
#             Product.objects.create(name=name, price=price, quantity=quantity)

#         return render(request, 'import_success.html')

#     return render(request, 'import_form.html')