from django.shortcuts import render, get_object_or_404, redirect
from django.http import request, JsonResponse, HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.db import transaction, models
from django.db.models import Q, Sum, Max, Min
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView, FormView, TemplateView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from viewflow.flow.views import FlowMixin


from my_portal.tooling import models, forms, serializers, widgets
from my_portal.projects.models import Supplier

from rest_framework import views
from rest_framework import generics

from rest_framework.response import Response

# Dashboard Views

@login_required
def dashboard(request):

    # Count of number of Tools
    num_tools = models.Tool.objects.all().count()
    # Production tools (status = 'PRODUCTION')
    num_production_tools = models.Tool.objects.filter(status__exact='Production').count()
    # Production tools (status = 'DEVELOPMENT')
    num_development_tools = models.Tool.objects.filter(status__exact='Development').count()

    watchlist = models.Tool.objects.filter(toolcondition__risk='Medium')

    context = {
        'num_tools': num_tools,
        'num_production_tools': num_production_tools,
        'num_development_tools': num_development_tools,
        'watchlist':watchlist,
    }

    return render(request, 'tooling/dashboard.html', context=context)

class Profile(LoginRequiredMixin, TemplateView):
    template_name = 'tooling/profile.html'


# Parts Views
class PartListView(LoginRequiredMixin, ListView):
    model = models.Part
    context_object_name = 'part_list'
    template_name = 'tooling/part_list.html'
    def get_queryset(self):
        queryset = self.model.objects.exclude(status='Obsolete')
        return queryset

class PartUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Part
    context_object_name = 'part_update'
    form_class = forms.PartUpdateForm
    template_name = 'tooling/part_update.html'
    success_url = reverse_lazy('tooling:part_list')

# Tools Views
class ToolListView(LoginRequiredMixin, ListView):
    model = models.Tool
    context_object_name = 'tool_list'
    template_name = 'tooling/tool_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['suppliers'] = Supplier.objects.all()
        return context

class ToolSupplierListView(LoginRequiredMixin, ListView):

    template_name = 'tooling/tool_list.html'
    context_object_name = 'tool_list'

    def get_queryset(self):
        self.supplier = get_object_or_404(Supplier, vendor_name=self.kwargs['vendor_name'])
        queryset = models.Tool.objects.filter(location=self.supplier)
        return queryset

    def get_context_data(self, **kwargs):
        self.supplier = get_object_or_404(Supplier, vendor_name=self.kwargs['vendor_name'])
        context = super().get_context_data(**kwargs)
        context['supplier'] = self.supplier
        return context

class ToolPartListView(LoginRequiredMixin, ListView):
    model = models.Tool
    template_name = 'tooling/tool_list.html'
    context_object_name = 'tool_list'

    def get_queryset(self):
        part = self.kwargs['part']
        queryset = self.model.objects.filter(part_produced__part_number=part)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        part = self.kwargs['part']
        context['part'] = part
        return context

class ToolCreateView(LoginRequiredMixin, CreateView):
    model = models.Tool
    form_class = forms.ToolForm
    template_name = 'tooling/tool_new.html'

class ToolDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Tool
    template_name = 'tooling/tool_delete.html'
    success_url = reverse_lazy('tooling:tool_list')

class ToolDetailView(LoginRequiredMixin, DetailView):
    model = models.Tool
    template_name = 'tooling/tool_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tool_inspected = self.kwargs['pk']
        last_risk = models.ToolCondition.objects.order_by('-date_assessment').filter(tool_inspected=tool_inspected)[0:1]
        context['last_risk'] = last_risk
        context['tool_inspected'] = tool_inspected
        return context 

class ToolUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Tool
    template_name = 'tooling/tool_update.html'
    form_class = forms.ToolForm

class ToolconditionFilterView(LoginRequiredMixin, FormView):
    template_name = 'tooling/toolcondition_filter.html'
    form_class = forms.FilterForm
    
    def get_success_url(self, **kwargs):
        vendor_pk = self.request.POST.get('vendor_pk',  default=None)
        year = self.request.POST.get('year_assessment',  default=None)
        return reverse_lazy('tooling:toolcondition_list_filter', kwargs={'vendor_pk': vendor_pk, 'year': year})

class ToolconditionListFilterView(LoginRequiredMixin, TemplateView):
    template_name = 'tooling/toolcondition_list_filter.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vendor_pk = self.kwargs['vendor_pk']
        year = self.kwargs['year']
        assessment_list = models.ToolCondition.objects.filter(tool_inspected__location=vendor_pk).filter(date_assessment__year=year).filter(~Q(tool_inspected__status='Stored')).distinct()
        context = {
            'assessment_list':assessment_list,
            'location':Supplier.objects.get(pk=vendor_pk),
            'year':year
        }
        return context

class ToolconditionCreateView(LoginRequiredMixin, CreateView):
    model = models.ToolCondition
    form_class = forms.ToolConditionForm
    template_name = 'tooling/toolcondition_new.html'

    def get_initial(self):
        return {'tool_inspected': self.kwargs['pk']}

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['tool'] = models.Tool.objects.get(tool_serial_number=self.kwargs['pk'])
        return context

class ToolConditionProcessCreateView(LoginRequiredMixin, FlowMixin, CreateView):
    model = models.ToolCondition
    form_class = forms.ToolConditionProcessForm
    template_name = 'tooling/toolcondition_new.html'

    def form_valid(self, form):
        tool_condition_data = form.save(commit=False)
        tool_condition_data.tool_inspected.location = self.activation.process.supplier
        tool_condition_data.save()
        self.activation_done()
        return redirect(self.get_success_url())

class ToolconditionUpdateView(LoginRequiredMixin, UpdateView):
    model = models.ToolCondition
    template_name = 'tooling/toolcondition_update.html'
    form_class = forms.ToolConditionForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tool'] = models.Tool.objects.get(tool_serial_number=self.kwargs['tool_pk'])
        return context

# API Views

class ToolListAPIView(generics.ListAPIView):

    serializer_class = serializers.ToolSerializer
    queryset = models.Tool.objects.all()

class ToolConditionListAPIView(generics.ListAPIView):

    serializer_class = serializers.ToolConditionSerializer
    queryset = models.ToolCondition.objects.all()

class ToolConditionAPIView(views.APIView):

    def get (self, request, format=None, **kwargs):
        tool_inspected = self.kwargs['tool_inspected']
        condition = models.ToolCondition.objects.filter(tool_inspected=tool_inspected)
        serializer = serializers.ToolConditionSerializer(condition, many=True)
        return Response(serializer.data)

