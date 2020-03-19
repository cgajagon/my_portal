from django.shortcuts import render, get_object_or_404
from django.db import models
from django.db.models import Q, Sum, Max, Min, Count
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from my_portal.projects import models, forms

# Dashboard Views

@login_required
def dashboard(request):

    if request.user.is_superuser == False:
        queryprojects = models.Project.objects.exclude(Q(status='Completed') | Q(status='Canceled')).filter(project_manager=request.user)
        querycosts = models.ProjectCost.objects.exclude(Q(project_related__status='Completed') | Q(project_related__status='Canceled')).filter(project_related__project_manager=request.user)
        queryjournal = models.ProjectJournal.objects.filter(project_related__project_manager=request.user)

    else:
        queryprojects = models.Project.objects.exclude(Q(status='Completed') | Q(status='Canceled'))
        querycosts = models.ProjectCost.objects.exclude(Q(project_related__status='Completed') | Q(project_related__status='Canceled')).filter(project_related__project_manager=request.user)
        queryjournal = models.ProjectJournal.objects.all()

    # Count of number of Projects
    num_projects = queryprojects.count()
    # Active Projects (status = 'Active')
    num_active_projects = queryprojects.filter(status__exact='Active').count()
    # Queued Projects (status = 'Queued')
    num_queued_projects = queryprojects.filter(status__exact='Queued').count()
    # Inactive Projects (status = 'Inactive')
    num_inactive_projects = queryprojects.filter(status__exact='Inactive').count()
    # Activities Due Soon
    activities = queryjournal.exclude(is_completed=True).order_by('due_date')[:10]
    # Costs
    totalcost = models.ProjectCost.objects.aggregate(Sum('amount'))
    querycostsbyprojectvendor = querycosts.values('project_related__customer__vendor_name')
    suppliercosts = querycostsbyprojectvendor.annotate(cost=Sum('amount'), proportion=100*Sum('amount')/totalcost['amount__sum']).order_by('-proportion')[:6]
    # Projects
    supplierprojects = queryprojects.exclude(status='Inactive').values('customer__vendor_name').annotate(count=Count('pk')).order_by('-count')[:8]

    context = {
        'num_projects': num_projects,
        'num_active_projects': num_active_projects,
        'num_queued_projects': num_queued_projects,
        'num_inactive_projects': num_inactive_projects,
        'activities': activities,
        'suppliercosts':suppliercosts,
        'supplierprojects':supplierprojects,
    }

    return render(request, 'projects/dashboard.html', context=context)

# Project Views

class ProjectListView(LoginRequiredMixin, ListView):
    model = models.Project
    context_object_name = 'project_list'
    template_name = 'projects/project_list.html'
  
    def get_queryset(self):
        if self.request.user.is_superuser == False:
            queryset = self.model.objects.exclude(Q(status='Completed') | Q(status='Canceled')).filter(project_manager=self.request.user).order_by('end_date').order_by('status')
        else:
            queryset = self.model.objects.exclude(Q(status='Completed') | Q(status='Canceled')).order_by('status')
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['suppliers'] = models.Supplier.objects.all()
        return context

class ProjectListFilterSupplierView(LoginRequiredMixin, ListView):
    model = models.Project
    context_object_name = 'project_list'
    template_name = 'projects/project_list.html'
  
    def get_queryset(self):
        self.supplier = get_object_or_404(models.Supplier, vendor_name=self.kwargs['vendor_name'])
        q = self.model.objects.exclude(Q(status='Completed') | Q(status='Canceled')).order_by('status')
        if self.request.user.is_superuser == False:
            queryset = q.filter(project_manager=self.request.user).order_by('end_date').filter(customer=self.supplier)
        else:
            queryset = q.filter(customer=self.supplier)
        return queryset
    
    def get_context_data(self, **kwargs):
        self.supplier = get_object_or_404(models.Supplier, vendor_name=self.kwargs['vendor_name'])
        context = super().get_context_data(**kwargs)
        context['supplier'] = self.supplier
        return context

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = models.Project
    form_class = forms.ProjectForm
    template_name = 'projects/project_new.html'

    def get_initial(self):
        initial = super(ProjectCreateView, self).get_initial()
        initial['project_manager'] = self.request.user
        return initial

class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Project
    template_name = 'projects/project_delete.html'
    success_url = reverse_lazy('projects:project_list')

class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = models.Project
    template_name = 'projects/project_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.kwargs['pk']
        context['cost'] = models.ProjectCost.objects.filter(project_related=project).aggregate(total_cost=Sum('amount'))
        specific_projects = models.ProjectMilestone.objects.filter(project_related=project)
        weeks = 0
        if specific_projects:
            min_start = specific_projects.aggregate(min_start=Min('start_date'))
            max_due = specific_projects.aggregate(max_due=Max('due_date'))
            weeks = (max_due['max_due']-min_start['min_start']).days/7
        context['duration'] = round(weeks)
        return context

class ProjectUpdateStatusView(LoginRequiredMixin, UpdateView):
    model = models.Project
    fields = ('status',)
    template_name = 'projects/project_update_status.html'
    success_url = reverse_lazy('projects:project_list')

class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Project
    form_class = forms.ProjectForm
    template_name = 'projects/project_update.html'

class ProjectJournalCreateView(LoginRequiredMixin, CreateView):
    model = models.ProjectJournal
    template_name = 'projects/projectjournal_edit.html'
    form_class = forms.ProjectJournalForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project_related'] = self.kwargs['project_pk']
        return context
    
    def get_initial(self, **kwargs):
        initial = super(ProjectJournalCreateView, self).get_initial()
        initial['project_related'] = self.kwargs['project_pk']
        return initial

class ProjectJournalUpdateView(LoginRequiredMixin, UpdateView):
    model = models.ProjectJournal
    form_class = forms.ProjectJournalForm
    template_name = 'projects/projectjournal_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project_related'] = self.kwargs['project_pk']
        return context

class ProjectJournalUpdateStatusView(LoginRequiredMixin, UpdateView):
    model = models.ProjectJournal
    form_class = forms.ProjectJournalForm
    template_name = 'projects/projectjournal_edit_status.html'
    success_url = reverse_lazy('projects:dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project_related'] = self.kwargs['project_pk']
        return context

class ProjectJournalDeleteView(LoginRequiredMixin, DeleteView):
    model = models.ProjectJournal
    template_name = 'projects/projectjournal_delete.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.kwargs['project_pk']
        context['project_pk'] = project
        return context

    def get_success_url(self, **kwargs):
        project=self.kwargs['project_pk']
        return reverse_lazy('projects:project_detail', kwargs={'pk':project})

class ProjectCostCreateView(LoginRequiredMixin, CreateView):
    model = models.ProjectCost
    template_name = 'projects/projectcost_edit.html'
    form_class = forms.ProjectCostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project_related'] = self.kwargs['project_pk']
        return context
    
    def get_initial(self, **kwargs):
        initial = super(ProjectCostCreateView, self).get_initial()
        initial['project_related'] = self.kwargs['project_pk']
        return initial

class ProjectCostUpdateView(LoginRequiredMixin, UpdateView):
    model = models.ProjectCost
    form_class = forms.ProjectCostForm
    template_name = 'projects/projectcost_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project_related'] = self.kwargs['project_pk']
        return context

class ProjectCostDeleteView(LoginRequiredMixin, DeleteView):
    model = models.ProjectCost
    template_name = 'projects/projectcost_delete.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.kwargs['project_pk']
        context['project_pk'] = project
        return context

    def get_success_url(self, **kwargs):
        project=self.kwargs['project_pk']
        return reverse_lazy('projects:project_detail', kwargs={'pk':project})

class ProjectMilestoneCreateView(LoginRequiredMixin, CreateView):
    model = models.ProjectMilestone
    form_class = forms.ProjectMilestoneForm
    template_name = 'projects/projectmilestone_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project_related'] = self.kwargs['project_pk']
        return context
    
    def get_initial(self, **kwargs):
        initial = super(ProjectMilestoneCreateView, self).get_initial()
        initial['project_related'] = self.kwargs['project_pk']
        return initial

class ProjectMilestoneUpdateView(LoginRequiredMixin, UpdateView):
    model = models.ProjectMilestone
    form_class = forms.ProjectMilestoneForm
    template_name = 'projects/projectmilestone_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project_related'] = self.kwargs['project_pk']
        return context

class ProjectMilestoneDeleteView(LoginRequiredMixin, DeleteView):
    model = models.ProjectMilestone
    template_name = 'projects/projectmilestone_delete.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.kwargs['project_pk']
        context['project_pk'] = project
        return context

    def get_success_url(self, **kwargs):
        project = self.kwargs['project_pk']
        return reverse_lazy('projects:project_detail', kwargs={'pk':project})

class ProjectDocumentView(FormView):
    form_class = forms.ProjectDocumentForm
    template_name = 'projects/projectdocument_upload.html'
    success_url = reverse_lazy('projects:project_list')
      
    def form_valid(self, form):
        form.save(commit=True)
        return super(ProjectDocumentView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.kwargs['project_pk']
        context['project_pk'] = project
        return context

    def get_initial(self,**kwargs):
        return {'project_related': self.kwargs['project_pk']}

class ProjectDocumentDeleteView(LoginRequiredMixin, DeleteView):
    model = models.ProjectDocument
    template_name = 'projects/projectdocument_delete.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.kwargs['project_pk']
        context['project_pk'] = project
        return context

    def get_success_url(self, **kwargs):
        project=self.kwargs['project_pk']
        return reverse_lazy('projects:project_detail', kwargs={'pk':project})

class ProjectListArchiveView(LoginRequiredMixin, ListView):
    model = models.Project
    context_object_name = 'project_list'
    template_name = 'projects/project_list.html'
  
    def get_queryset(self):
        if self.request.user.is_superuser == False:
            queryset = self.model.objects.exclude(Q(status='Active') | Q(status='Queued') | Q(status='Inactive')).filter(project_manager=self.request.user).order_by('end_date').order_by('status')
        else:
            queryset = self.model.objects.exclude(Q(status='Active') | Q(status='Queued') | Q(status='Inactive')).order_by('status')
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['suppliers'] = models.Supplier.objects.all()
        return context
