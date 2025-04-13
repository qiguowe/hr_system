from django.contrib import admin
from .models import Company, Project, Resume, ResumeProject, ProjectStatus, ResumeStatus, Tag, PaymentRecord

@admin.register(ProjectStatus)
class ProjectStatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'order', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'code')
    ordering = ('order', 'created_at')

@admin.register(ResumeStatus)
class ResumeStatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'order', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'code')
    ordering = ('order', 'created_at')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'created_by', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'contact_phone', 'created_at', 'created_by')
    list_filter = ('created_at',)
    search_fields = ('name', 'contact_person', 'contact_phone', 'contact_email')
    date_hierarchy = 'created_at'

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'job_title', 'status', 'created_at', 'created_by')
    list_filter = ('status', 'created_at', 'company')
    search_fields = ('title', 'job_title', 'company__name')
    date_hierarchy = 'created_at'

@admin.register(PaymentRecord)
class PaymentRecordAdmin(admin.ModelAdmin):
    list_display = ('project', 'amount', 'payment_date', 'payment_method', 'created_by')
    list_filter = ('payment_date', 'payment_method')
    search_fields = ('project__title', 'description')
    date_hierarchy = 'payment_date'

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender', 'phone', 'email', 'education', 'experience_years', 'created_at', 'created_by')
    list_filter = ('gender', 'education', 'created_at', 'tags')
    search_fields = ('name', 'phone', 'email', 'school', 'current_company')
    date_hierarchy = 'created_at'
    filter_horizontal = ('tags',)

@admin.register(ResumeProject)
class ResumeProjectAdmin(admin.ModelAdmin):
    list_display = ('resume', 'project', 'status', 'submitted_at')
    list_filter = ('status', 'submitted_at')
    search_fields = ('resume__name', 'project__title', 'project__company__name')
    date_hierarchy = 'submitted_at'
