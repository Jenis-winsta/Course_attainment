from import_export import resources
from .models import Student

class StudentResource(resources.ModelResource):
    class Meta:
        model = Student
        fields = '__all__'
        
        
        # resources.py
# from import_export import resources
# from .models import Student

# class StudentResource(resources.ModelResource):
#     class Meta:
#         model = Student
#         import_id_fields = ['id']
