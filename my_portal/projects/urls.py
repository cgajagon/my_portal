from django.urls import path
from my_portal.projects import views

app_name = 'projects'
urlpatterns = [

    #Dashboard
    path('', views.dashboard, name='dashboard'),

    #Projects
    path('list/', views.ProjectListView.as_view(), name='project_list'),
    path('list/<vendor_name>', views.ProjectListFilterSupplierView.as_view(), name='project_list_supplier'),
    path('details/<int:pk>', views.ProjectDetailView.as_view(), name='project_detail'),
    path('new/', views.ProjectCreateView.as_view(), name='project_create'),
    path('update/<int:pk>', views.ProjectUpdateView.as_view(), name='project_update'),
    path('status/<int:pk>', views.ProjectUpdateStatusView.as_view(), name='project_update_status'),
    path('delete/<int:pk>', views.ProjectDeleteView.as_view(), name='project_delete'),
    path('<int:project_pk>/journal/new', views.ProjectJournalCreateView.as_view(), name='projectjournal_create'),
    path('<int:project_pk>/journal/edit/<int:pk>', views.ProjectJournalUpdateView.as_view(), name='projectjournal_edit'),
    path('<int:project_pk>/journal/status/<int:pk>', views.ProjectJournalUpdateStatusView.as_view(), name='projectjournal_edit_status'),
    path('<int:project_pk>/journal/delete/<int:pk>', views.ProjectJournalDeleteView.as_view(), name='projectjournal_delete'),
    path('<int:project_pk>/cost/new', views.ProjectCostCreateView.as_view(), name='projectcost_create'),
    path('<int:project_pk>/cost/edit/<int:pk>', views.ProjectCostUpdateView.as_view(), name='projectcost_edit'),
    path('<int:project_pk>/cost/delete/<int:pk>', views.ProjectCostDeleteView.as_view(), name='projectcost_delete'),
    path('<int:project_pk>/milestone/new', views.ProjectMilestoneCreateView.as_view(), name='projectmilestone_create'),
    path('<int:project_pk>/milestone/edit/<int:pk>', views.ProjectMilestoneUpdateView.as_view(), name='projectmilestone_edit'),
    path('<int:project_pk>/milestone/delete/<int:pk>', views.ProjectMilestoneDeleteView.as_view(), name='projectmilestone_delete'),
    path('<int:project_pk>/document/upload', views.ProjectDocumentView.as_view(), name='projectdocument_upload'),
    path('<int:project_pk>/document/delete/<int:pk>', views.ProjectDocumentDeleteView.as_view(), name='projectdocument_delete'),
    path('archive/', views.ProjectListArchiveView.as_view(), name='project_list_archive'),
]