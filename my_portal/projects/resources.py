from django.db import IntegrityError

from my_portal.projects import models
from import_export import resources, fields, widgets

class SupplierResource(resources.ModelResource):
    class Meta:
        model = models.Supplier

class ProjectResource(resources.ModelResource):
    customer = fields.Field(
        attribute='customer',
        column_name='customer',
        widget=widgets.ForeignKeyWidget(models.Supplier, 'vendor_name'))
    
    class Meta:
        model = models.Project