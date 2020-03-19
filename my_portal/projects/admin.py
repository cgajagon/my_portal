from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

from my_portal.projects import models, resources


class SupplierAdmin(ImportExportModelAdmin):
    resource_class = resources.SupplierResource

class ProjectAdmin(ImportExportModelAdmin):
    resource_class = resources.ProjectResource

admin.site.register(models.Supplier, SupplierAdmin)
admin.site.register(models.Project, ProjectAdmin)