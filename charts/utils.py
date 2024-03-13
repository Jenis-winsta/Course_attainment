import pandas as pd
from .models import Student
from tablib import Dataset




def process_excel_file(file):
    xl = pd.ExcelFile(file)
    dfs=[]
    for sheet_name in xl.sheet_names:  # Iterate over sheet names
        df = pd.read_excel(file, sheet_name=sheet_name)  # Read data from current sheet
        dfs.append(df)
        data = df.to_dict(orient='records')
        for row in data:
            student = Student.objects.create(
                name=row.get('Student', 'a'),
                cia_marks=row.get('CIA', 0),
                sem_marks=row.get('End Sem', 0),
                total_marks=row.get('Total', 0),
                file_name=sheet_name  # Use sheet name as file_name field value
            )
            student.save()
        return dfs

'''
def process_excel_file(file):
    dataset = Dataset()
    xl = pd.ExcelFile(file)
    for sheet_name in xl.sheet_names:
        df = pd.read_excel(file, sheet_name=sheet_name)
        for _,row in df.iterrows():
            student = Student.objects.create(
                name=row['Student'],
                cia_marks=row['CIA'],
                sem_marks=row['End Sem'],
                total_marks=row['Total'],
                file_name=sheet_name
            )
            student.save()

'''