import datetime

from django.db import models
from django.urls import reverse_lazy
from my_portal.users.models import User

class Supplier(models.Model):
    USA = 'USA'
    CAN = 'CANADA'
    OTH = 'OTHER'
    COUNTRY = [
        (USA, 'USA'),
        (CAN, 'CANADA'),
        (OTH, 'OTHER'),
    ]
    vendor_code = models.IntegerField(null=False, blank=False, unique=True)
    vendor_name = models.CharField(max_length=200, null=False, blank=False)
    country = models.CharField(max_length=10, choices=COUNTRY, default=CAN)
    account_manager = models.ForeignKey(User, on_delete=models.SET_NULL, null= True, blank=True)

    class Meta:
        ordering = ['vendor_name']

    def __str__(self):
        return self.vendor_name

class Project(models.Model):
    QUEUED = 'Queued'
    ACTIVE = 'Active'
    INACTIVE = 'Inactive'
    CANCELED = 'Canceled'
    COMPLETED = 'Completed'
    STATUS = [
        (QUEUED, 'Queued'),
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
        (CANCELED, 'Canceled'),
        (COMPLETED, 'Completed'),
    ]

    REGULAR = 'Regular'
    COMPLEX = 'Complex'
    COMPLEXITY = [
        (REGULAR, 'Regular'),
        (COMPLEX, 'Complex'),
    ]

    C1 = 'Machining'
    C2 = 'Composites and Fabrications'
    C5 = 'Structural Castings'
    C6 = 'Blades'
    C8 = 'Vanes and Rings'
    COMMODITY = [
        (C1, 'Machining'),
        (C2, 'Composites and Fabrications'),
        (C5, 'Structural Castings'),
        (C6, 'Blades'),
        (C8, 'Vanes and Rings'),
    ]

    finance_ID = models.IntegerField(null=False, blank=False, default=0)
    title = models.CharField(max_length=200, null=False, blank=False)
    customer = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=False, blank=False)
    part_number_affected = models.CharField(max_length=200, null=False, blank=False)
    tool_serial_number_affected = models.CharField(max_length=200, null=True, blank=True)
    project_description = models.TextField(max_length=400, null=False, blank=False)
    project_justification = models.TextField(max_length=400, null=False, blank=False)
    start_date = models.DateField(null=False, blank=False, default=datetime.date.today)
    end_date = models.DateField(null=False, blank=False)
    constraint_end_date = models.DateField(null=True, blank=True)
    project_manager = models.ForeignKey(User, on_delete=models.SET_NULL, null= True, blank=True)
    design_job = models.CharField(max_length=25, null=True, blank=True, unique=True)
    commodity = models.CharField(max_length=50, choices=COMMODITY)
    complexity = models.CharField(max_length=10, choices=COMPLEXITY, default=REGULAR)
    status = models.CharField(max_length=10, choices=STATUS, default=QUEUED)
   
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('projects:project_detail', args=[self.pk])

    class Meta:
        permissions = (
            ('can_view_project', 'Can view project'),
        )

class ProjectJournal(models.Model):
    project_related = models.ForeignKey(Project, on_delete=models.CASCADE, null=False, blank=False)
    title = models.CharField(max_length=100, null=False, blank=False)
    comment = models.TextField(max_length=500, null=True, blank=True)
    entry_date = models.DateField(null=False, blank=False, default=datetime.date.today)
    due_date = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-entry_date', '-due_date']
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('projects:project_detail', args=[self.project_related.pk])

class ProjectMilestone(models.Model):
    project_related = models.ForeignKey(Project, on_delete=models.CASCADE, null=False, blank=False)
    milestone = models.CharField(max_length=200, null=False, blank=False)
    comment = models.TextField(max_length=200, null=True, blank=True)
    start_date = models.DateField(null=False, blank=False)
    due_date = models.DateField(null=False, blank=False)
    is_completed = models.BooleanField()

    class Meta:
        ordering = ['-start_date']

    def duration(self):
        days = (self.due_date-self.start_date).days
        duration = round(days/7,0)
        return duration

    def __str__(self):
        return self.milestone

    def get_absolute_url(self):
        return reverse_lazy('projects:project_detail', args=[self.project_related.pk])

class ProjectCost(models.Model):
    
    CAD = 'CAD'
    USD = 'USD'
    OTHER='OTHER'
    CURRENCY = [
        (CAD, 'CAD'),
        (USD, 'USD'),
        (OTHER, 'Other')
    ]

    CAPEX = 'CAPEX'
    OPEX = 'OPEX'
    EXPENSE = [
        (CAPEX, 'CAPEX'),
        (OPEX, 'OPEX'),
    ]  
    
    description = models.TextField(max_length=200, null=False, blank=False)
    project_related = models.ForeignKey(Project, on_delete=models.CASCADE, null=False, blank=False)
    amount = models.FloatField(max_length=20, blank=False, null=False)
    currency = models.CharField(max_length=5, choices=CURRENCY, default=USD)
    expense_type = models.CharField(max_length=5, choices=EXPENSE, default=CAPEX)
    entry_date = models.DateField(null=False, blank=False, default=datetime.date.today)
    
    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse_lazy('projects:project_detail', args=[self.project_related.pk])

class ProjectDocument(models.Model):
    FORM10024 = 'Form 10024'
    FORM10141 = 'Form 10141'
    FORM11212 = 'Form 11212'
    FORM11248 = 'Form 11248'
    FORM11615 = 'Form 11615'
    FORM11674 = 'Form 11674'
    FORM12165 = 'Form 12165'
    INVOICE = 'Invoice'
    BUSINESSCASE = 'Business Case'
    QUOTE = 'Quote'
    CONTRACT = 'Contract'
    OTHER = 'Other'
    
    DOC = [
    (FORM10024,'Form 10024'),
    (FORM10141,'Form 10141'),
    (FORM11212,'Form 11212'),
    (FORM11248,'Form 1248'),
    (FORM11615,'Form 11615'),
    (FORM11674,'Form 11674'),
    (FORM12165,'Form 12165'),
    (INVOICE,'Invoice'),
    (BUSINESSCASE,'Business Case'),
    (QUOTE,'Quote'),
    (CONTRACT,'Contract'),
    (OTHER,'Other'),
    ]  

    project_related = models.ForeignKey(Project, on_delete=models.CASCADE, null=False, blank=False)
    title = models.CharField(max_length=255, blank=False)
    document_type = models.CharField(max_length=20, choices=DOC, default=OTHER)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)