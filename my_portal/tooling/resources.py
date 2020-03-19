from my_portal.tooling import models
from import_export import resources, fields, widgets
from django.db import IntegrityError

class ToolconditionResource(resources.ModelResource):
    tool_inspected = fields.Field(
        attribute='tool_inspected',
        column_name='tool_inspected',
        widget=widgets.ForeignKeyWidget(models.Tool, 'tool_serial_number'))

    class Meta:
        model = models.ToolCondition


class SupplierResource(resources.ModelResource):
    class Meta:
        model = models.Supplier

class PartResource(resources.ModelResource):
    class Meta:
        model = models.Part
        skip_unchanged = True

    def save_instance(self, instance, using_transactions=True, dry_run=False):
        try:
            super().save_instance(instance, using_transactions, dry_run)
        except IntegrityError:
            pass

class ToolResource(resources.ModelResource):
    location = fields.Field(
        attribute='location',
        column_name='location',
        widget=widgets.ForeignKeyWidget(models.Supplier, 'vendor_name'))
    
    part_produced = fields.Field(
        attribute='part_produced',
        column_name='part_produced',
        widget=widgets.ManyToManyWidget(models.Part, field='part_number'))

    class Meta:
        model = models.Tool
        import_id_fields = ('tool_serial_number',)