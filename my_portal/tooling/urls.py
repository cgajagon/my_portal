from django.urls import path, include
from my_portal.tooling import views
from rest_framework.routers import DefaultRouter

from viewflow.flow.viewset import FlowViewSet

from my_portal.tooling.flows import AuditFlow

# Create a router and register our viewsets with it.
router = DefaultRouter()
# router.register(r'tools', views.ToolViewSet)

# Set of URLS for the Tool Condtion Audit
audit_urls = FlowViewSet(AuditFlow).urls

app_name = 'tooling'
urlpatterns = [
    #Part
    path('parts/',views.PartListView.as_view(), name='part_list'),
    path('parts/<int:pk>',views.PartUpdateView.as_view(), name='part_update'),
    #Tooling 
    path('list/', views.ToolListView.as_view(), name='tool_list'),
    path('list/<vendor_name>/', views.ToolSupplierListView.as_view(), name='tool_list_by_supplier'),
    path('list/parts/<part>', views.ToolPartListView.as_view(), name='tool_part_list'),
    path('new', views.ToolCreateView.as_view(), name='tool_new'),
    path('details/<str:pk>', views.ToolDetailView.as_view(), name='tool_detail'),
    path('delete/<str:pk>', views.ToolDeleteView.as_view(), name='tool_delete'),
    path('update/<str:pk>', views.ToolUpdateView.as_view(), name='tool_update'),
    #Tooling Conditions
    path('toolcondition/list/', views.ToolconditionFilterView.as_view(), name='toolcondition_list_filter'),
    path('toolcondition/list/<int:vendor_pk>/<int:year>', views.ToolconditionListFilterView.as_view(), name='toolcondition_list_filter'),
    path('details/<str:pk>/toolcondition/new', views.ToolconditionCreateView.as_view(), name='toolcondition_new'),
    path('details/<str:tool_pk>/toolcondition/update/<int:pk>', views.ToolconditionUpdateView.as_view(), name='toolcondition_update'),
    #Tool Condition Audit
    path('audit/', include(audit_urls)),
    #API
    path('', include(router.urls)),
    path('API/tools', views.ToolListAPIView.as_view()),
    path('API/toolconditions', views.ToolConditionListAPIView.as_view()),
    path('API/toolconditions/<str:tool_inspected>', views.ToolConditionAPIView.as_view()),
]