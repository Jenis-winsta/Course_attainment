# for import export excel files from frontend
from import_export import resources
from .models import Data

class DataResource(resources.ModelResource):
    class Meta:
        model = Data 