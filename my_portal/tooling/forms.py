import datetime
from django import forms
from django.utils import timezone
from django.forms.models import inlineformset_factory, modelformset_factory

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

from my_portal.tooling import models
from my_portal.tooling import widgets


class PartForm(forms.ModelForm):
    class Meta:
        model = models.Part
        fields = ('part_number', 'revision', 'part_description')
        widgets = {
            'part_description': forms.Textarea(attrs={
                'rows':3
            }),
        }

class PartUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Part
        fields = ('status', 'part_description')
        widgets = {
            'part_description': forms.Textarea(attrs={
                'rows':3
            }),
        }

class FilterForm(forms.Form):
    vendor_pk = forms.ModelChoiceField(queryset=models.Supplier.objects.all(), label='Vendor Name')
    year_assessment = forms.IntegerField(initial=datetime.date.today().year, label='Year Assessment')

class ToolForm(forms.ModelForm):
    class Meta:
        model = models.Tool
        fields = '__all__'
        widgets = {
            'tool_description': forms.Textarea(attrs={
                'rows':3
            }),
            'part_produced': widgets.Select2MultipleWidget(attrs={
                'placeholder':'Your placeholder',
                'multiple':True,
                'maximum-selection-length': 3
            })
        }

class ToolConditionForm(forms.ModelForm):
    class Meta:
        model = models.ToolCondition
        fields = '__all__'
        widgets = {
            'comments': forms.Textarea(attrs={
                'rows':3
            }),
            'tool_inspected': forms.HiddenInput
        }

class ToolConditionProcessForm(forms.ModelForm):
    class Meta:
        model = models.ToolCondition
        fields = ["tool_condition", "life", "life_remaining", "parts_forecasted", "months_forecasted", "risk"]

class ApproveForm(forms.ModelForm):
    def save(self, commit=True):
        instance = super(ApproveForm, self).save(commit=False)
        instance.approved_at = timezone.now()
        if commit:
            instance.save()
        return instance

    class Meta:
        model = models.ToolConditionProcess
        fields = ['approved']