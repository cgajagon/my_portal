from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from my_portal.tooling.models import Tool, ToolCondition, Part
from my_portal.tooling import resources


class PartAdmin(ImportExportModelAdmin):
    resource_class = resources.PartResource

class ToolConditionAdmin(ImportExportModelAdmin):
    resource_class = resources.ToolconditionResource

class ToolAdmin(ImportExportModelAdmin):
    resource_class = resources.ToolResource

admin.site.register(ToolCondition, ToolConditionAdmin)
admin.site.register(Tool, ToolAdmin)
admin.site.register(Part, PartAdmin)
