from django import forms
from .models import Company, Project, Resume, ResumeProject, Tag, PaymentRecord, ProjectStatus, ResumeStatus

class StatusForm(forms.ModelForm):
    """状态表单基类"""
    class Meta:
        fields = ('name', 'code', 'description', 'order', 'is_active')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ProjectStatusForm(StatusForm):
    """项目状态表单"""
    class Meta(StatusForm.Meta):
        model = ProjectStatus

class ResumeStatusForm(StatusForm):
    """简历状态表单"""
    class Meta(StatusForm.Meta):
        model = ResumeStatus

class TagForm(forms.ModelForm):
    """标签表单"""
    class Meta:
        model = Tag
        fields = ('name', 'color')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
        }

class CompanyForm(forms.ModelForm):
    """公司表单"""
    class Meta:
        model = Company
        fields = ('name', 'address', 'contact_person', 'contact_phone', 'contact_email', 'description')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class ProjectForm(forms.ModelForm):
    """项目表单"""
    class Meta:
        model = Project
        fields = ('title', 'company', 'job_title', 'job_description', 'requirements', 
                  'salary_range', 'location', 'status', 'deadline')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'company': forms.Select(attrs={'class': 'form-control'}),
            'job_title': forms.TextInput(attrs={'class': 'form-control'}),
            'job_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'requirements': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'salary_range': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class PaymentRecordForm(forms.ModelForm):
    """回款记录表单"""
    class Meta:
        model = PaymentRecord
        fields = ('amount', 'payment_date', 'payment_method', 'description')
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'payment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'payment_method': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class ResumeForm(forms.ModelForm):
    """简历表单"""
    class Meta:
        model = Resume
        fields = [
            'name', 'gender', 'birth_date', 'phone', 'email',
            'education', 'school', 'major',
            'experience_years', 'current_company', 'current_position',
            'work_experience',
            'work_exp_1_company', 'work_exp_1_position', 'work_exp_1_period', 'work_exp_1_description',
            'work_exp_2_company', 'work_exp_2_position', 'work_exp_2_period', 'work_exp_2_description',
            'work_exp_3_company', 'work_exp_3_position', 'work_exp_3_period', 'work_exp_3_description',
            'skills', 'tags', 'resume_file'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'education': forms.Select(attrs={'class': 'form-select'}),
            'school': forms.TextInput(attrs={'class': 'form-control'}),
            'major': forms.TextInput(attrs={'class': 'form-control'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control'}),
            'current_company': forms.TextInput(attrs={'class': 'form-control'}),
            'current_position': forms.TextInput(attrs={'class': 'form-control'}),
            'work_experience': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'work_exp_1_company': forms.TextInput(attrs={'class': 'form-control'}),
            'work_exp_1_position': forms.TextInput(attrs={'class': 'form-control'}),
            'work_exp_1_period': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '例如: 2018年6月 - 2020年8月'}),
            'work_exp_1_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'work_exp_2_company': forms.TextInput(attrs={'class': 'form-control'}),
            'work_exp_2_position': forms.TextInput(attrs={'class': 'form-control'}),
            'work_exp_2_period': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '例如: 2016年3月 - 2018年5月'}),
            'work_exp_2_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'work_exp_3_company': forms.TextInput(attrs={'class': 'form-control'}),
            'work_exp_3_position': forms.TextInput(attrs={'class': 'form-control'}),
            'work_exp_3_period': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '例如: 2014年9月 - 2016年2月'}),
            'work_exp_3_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'skills': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-select', 'multiple': 'multiple'}),
            'resume_file': forms.FileInput(attrs={'class': 'form-control'}),
        }

class ResumeSubmissionForm(forms.ModelForm):
    """简历投递表单"""
    class Meta:
        model = ResumeProject
        fields = ('status', 'notes')
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class SubmissionStatusForm(forms.ModelForm):
    """投递状态更新表单"""
    class Meta:
        model = ResumeProject
        fields = ('status', 'notes')
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        } 