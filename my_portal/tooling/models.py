import datetime

from django.db import models
from django.urls import reverse_lazy
from viewflow.models import Process

from my_portal.projects.models import Supplier

class Part(models.Model):
    DEVELOPMENT = 'In Development'
    RELEASED = 'Released'
    OBSOLETE = 'Obsolete'
    STATUS = [
        (DEVELOPMENT, 'In Development'),
        (RELEASED, 'Released'),
        (OBSOLETE, 'Obsolete'),
    ]

    part_number = models.CharField(max_length=200, null=False, blank=False)
    revision = models.CharField(max_length=3, default='-')
    part_description = models.TextField(max_length=400)
    status = models.CharField(max_length=20, choices=STATUS, default=DEVELOPMENT)
    
    def __str__(self):
        return '%s %s' % (self.part_number, self.revision)

class Tool(models.Model):
    DEVELOPMENT = 'Development'
    PRODUCTION = 'Production'
    STORED = 'Stored'
    STATUS = [
        (DEVELOPMENT, 'Development'),
        (PRODUCTION, 'Production'),
        (STORED, 'Stored'),
    ]

    tool_serial_number = models.CharField(max_length=20, primary_key=True)
    tool_cavitiy_numbers = models.CharField(max_length=10, null=True, blank=True)
    tool_description = models.TextField(max_length=400)
    location = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=False, blank=False)
    part_produced = models.ManyToManyField(Part)
    year_built = models.IntegerField(null=False, blank=False)
    is_audit_required = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=STATUS, default=DEVELOPMENT)

    def get_absolute_url(self):
        return reverse_lazy('tooling:tool_detail', args=[self.pk])

    def get_last_condition(self):
        return self.toolcondition_set.order_by('-date_assessment')[:1]
    
    def __str__(self):
        return self.tool_serial_number

class ToolCondition(models.Model):
    NEW = 'New'
    GOOD = 'Good'
    FAIR = 'Fair'
    POOR = 'Poor'
    WEAROUT = 'Wear-Out'
    TOOL_CONDITION = [
        (NEW, 'New'),
        (GOOD, 'Good'),
        (FAIR, 'Fair'),
        (POOR, 'Poor'),
        (WEAROUT, 'Wear-Out'),
    ]

    LOW = 'Low'
    MEDIUM = 'Medium'
    HIGH = 'High'
    RISK = [
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High'),
    ]

    tool_inspected = models.ForeignKey(Tool, on_delete=models.CASCADE, null=False, blank=False)
    tool_condition = models.CharField(max_length=10, choices=TOOL_CONDITION, default=NEW)
    life = models.IntegerField(null=False, blank=False)
    life_remaining = models.IntegerField(null=False, blank=False)
    tool_yield = models.FloatField(null=False, blank=False, default=0.95)
    parts_forecasted = models.IntegerField(null=False, blank=False)
    months_forecasted = models.IntegerField(null=False, blank=False)
    comments = models.TextField(null=True, blank=True)
    date_assessment = models.DateField(null=False, blank=False, default=datetime.date.today)
    risk = models.CharField(max_length=8, choices=RISK, default=LOW)

    def get_risk_evaluated(self):
        if self.months_forecasted != 0:
            ratio = (self.life_remaining / (self.parts_forecasted / self.months_forecasted)) / 12
        else:
            ratio = 0

        return ratio

    def get_absolute_url(self):
        return reverse_lazy('tooling:tool_detail', args=[self.tool_inspected.pk])

class ToolConditionProcess(Process):
    tool_inspected = models.ForeignKey(Tool, blank=True, null=True, on_delete=models.CASCADE)
    date_audit = models.DateTimeField(null=True)
    approved = models.BooleanField(default=False)
    approved_at = models.DateTimeField(null=True)