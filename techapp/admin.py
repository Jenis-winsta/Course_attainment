from django.contrib import admin

from . models import *
# Register your models here.

admin.site.register(Year)
admin.site.register(Semester)

admin.site.register(Department)

admin.site.register(Programme)
admin.site.register(Programme_Outcome)

admin.site.register(Programme_Specific)
admin.site.register(Programme_Specific_Outcome)


admin.site.register(Course)
admin.site.register(Course_Outcome)


# Register your models here.

