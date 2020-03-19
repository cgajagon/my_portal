from django import forms
from my_portal.projects import models

class ProjectForm(forms.ModelForm):
    class Meta:

        model = models.Project
        fields = '__all__'
        widgets = {
            'project_description': forms.Textarea(attrs={
                'rows':3,
            }),
            'project_justification': forms.Textarea(attrs={
                'rows':3,
            })
        }

class ProjectJournalForm(forms.ModelForm):
    class Meta:
        model = models.ProjectJournal
        fields = '__all__'
        widgets = {
            'comment': forms.Textarea(attrs={
                'rows':3
            }),
            'project_related': forms.HiddenInput,
            'entry_date': forms.HiddenInput,
            'project_manager': 1

        }

class ProjectCostForm(forms.ModelForm):
    class Meta:
        model = models.ProjectCost
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={
                'rows':2
            }),
            'project_related': forms.HiddenInput,
            'entry_date': forms.HiddenInput
        }

class ProjectMilestoneForm(forms.ModelForm):
    class Meta:
        model = models.ProjectMilestone
        fields = '__all__'
        widgets = {
            'comment': forms.Textarea(attrs={
                'rows':2
            }),
            'project_related': forms.HiddenInput,
        }

class ProjectDocumentForm(forms.ModelForm):
    class Meta:
        model = models.ProjectDocument
        fields = '__all__'
        widgets = {
            'project_related': forms.HiddenInput,
        }