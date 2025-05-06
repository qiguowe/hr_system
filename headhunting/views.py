from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden, JsonResponse, FileResponse, HttpResponse
from django.db.models import Q, Count, Sum
from .models import (
    Company, Project, Resume, ResumeProject, 
    Tag, PaymentRecord, ProjectStatus, ResumeStatus, ResumeBookmark
)
from .forms import (
    CompanyForm, ProjectForm, ResumeForm, ResumeSubmissionForm, 
    SubmissionStatusForm, TagForm, PaymentRecordForm, 
    ProjectStatusForm, ResumeStatusForm
)
from accounts.decorators import admin_required, system_admin_required
from django.urls import reverse
from .utils import ResumeParser
import os
import tempfile
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import time
import mimetypes

# Create your views here.

# 公司管理视图
@login_required
def company_list(request):
    """公司列表视图"""
    companies = Company.objects.all()
    # 所有用户都可以看到所有公司
    
    # 搜索功能
    query = request.GET.get('q')
    if query:
        companies = companies.filter(
            Q(name__icontains=query) | 
            Q(contact_person__icontains=query) | 
            Q(address__icontains=query)
        )
    
    return render(request, 'headhunting/company_list.html', {'companies': companies})

@login_required
def company_create(request):
    """创建公司视图 - 所有用户都可以创建公司"""
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            company = form.save(commit=False)
            company.created_by = request.user
            company.save()
            messages.success(request, '公司创建成功')
            return redirect('company_list')
    else:
        form = CompanyForm()
    
    return render(request, 'headhunting/company_form.html', {'form': form, 'title': '创建公司'})

@login_required
def company_detail(request, pk):
    """公司详情视图"""
    company = get_object_or_404(Company, pk=pk)
    
    # 所有已登录用户都可以查看公司详情
    
    return render(request, 'headhunting/company_detail.html', {'company': company})

@admin_required
def company_update(request, pk):
    """更新公司视图 - 需要管理员权限"""
    company = get_object_or_404(Company, pk=pk)
    
    # 检查权限
    if not (request.user.is_system_admin or request.user.is_admin) and company.created_by != request.user:
        return HttpResponseForbidden('您没有权限编辑此公司')
    
    if request.method == 'POST':
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            messages.success(request, '公司更新成功')
            return redirect('company_detail', pk=company.pk)
    else:
        form = CompanyForm(instance=company)
    
    return render(request, 'headhunting/company_form.html', {'form': form, 'title': f'编辑公司: {company.name}'})

@admin_required
def company_delete(request, pk):
    """删除公司视图 - 需要管理员权限"""
    company = get_object_or_404(Company, pk=pk)
    
    # 检查权限
    if not (request.user.is_system_admin or request.user.is_admin) and company.created_by != request.user:
        return HttpResponseForbidden('您没有权限删除此公司')
    
    if request.method == 'POST':
        company.delete()
        messages.success(request, '公司删除成功')
        return redirect('company_list')
    
    return render(request, 'headhunting/company_confirm_delete.html', {'company': company})

# 项目管理视图
@login_required
def project_list(request):
    """项目列表视图"""
    projects = Project.objects.all()
    # 所有用户都可以看到所有项目
    
    # 搜索功能
    query = request.GET.get('q')
    if query:
        projects = projects.filter(
            Q(title__icontains=query) | 
            Q(job_title__icontains=query) | 
            Q(company__name__icontains=query)
        )
    
    return render(request, 'headhunting/project_list.html', {'projects': projects})

@login_required
def project_create(request):
    """创建项目视图 - 所有用户都可以创建项目"""
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()
            messages.success(request, '项目创建成功')
            return redirect('project_list')
    else:
        form = ProjectForm()
        # 限制公司选择
        if not request.user.is_system_admin:
            form.fields['company'].queryset = Company.objects.filter(
                Q(created_by=request.user) | Q(created_by__user_type='system_admin')
            )
    
    return render(request, 'headhunting/project_form.html', {'form': form, 'title': '创建项目'})

@login_required
def project_detail(request, pk):
    """项目详情视图"""
    project = get_object_or_404(Project, pk=pk)
    
    # 所有已登录用户都可以查看项目详情
    
    # 获取已投递到该项目的简历
    submissions = project.resume_submissions.all()
    
    return render(request, 'headhunting/project_detail.html', {
        'project': project,
        'submissions': submissions
    })

@admin_required
def project_update(request, pk):
    """更新项目视图 - 需要管理员权限"""
    project = get_object_or_404(Project, pk=pk)
    
    # 检查权限
    if not (request.user.is_system_admin or request.user.is_admin) and project.created_by != request.user:
        return HttpResponseForbidden('您没有权限编辑此项目')
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, '项目更新成功')
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectForm(instance=project)
        # 限制公司选择
        if not request.user.is_system_admin:
            form.fields['company'].queryset = Company.objects.filter(
                Q(created_by=request.user) | Q(created_by__user_type='system_admin')
            )
    
    return render(request, 'headhunting/project_form.html', {'form': form, 'title': f'编辑项目: {project.title}'})

@admin_required
def project_delete(request, pk):
    """删除项目视图 - 需要管理员权限"""
    project = get_object_or_404(Project, pk=pk)
    
    # 检查权限
    if not (request.user.is_system_admin or request.user.is_admin) and project.created_by != request.user:
        return HttpResponseForbidden('您没有权限删除此项目')
    
    if request.method == 'POST':
        project.delete()
        messages.success(request, '项目删除成功')
        return redirect('project_list')
    
    return render(request, 'headhunting/project_confirm_delete.html', {'project': project})

# 简历管理视图
@login_required
def resume_list(request):
    """简历列表视图"""
    resumes = Resume.objects.all()
    if not request.user.is_system_admin and not request.user.is_admin:
        # 普通用户只能看到自己创建的简历
        resumes = resumes.filter(created_by=request.user)
    
    # 搜索功能
    query = request.GET.get('q')
    if query:
        resumes = resumes.filter(
            Q(name__icontains=query) | 
            Q(phone__icontains=query) | 
            Q(email__icontains=query) | 
            Q(current_company__icontains=query) |
            Q(current_position__icontains=query)
        )
    
    # 获取活跃的项目供投递使用
    projects = Project.objects.filter(status__code='active')
    
    return render(request, 'headhunting/resume_list.html', {
        'resumes': resumes,
        'projects': projects
    })

@login_required
def resume_create(request):
    """创建简历视图"""
    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.created_by = request.user
            
            # 检查是否有暂存的文件
            temp_file_path = request.session.get('temp_resume_file')
            if temp_file_path and os.path.exists(temp_file_path):
                with open(temp_file_path, 'rb') as f:
                    resume.resume_file.save(
                        request.session.get('temp_resume_filename', 'resume.pdf'),
                        ContentFile(f.read()),
                        save=False
                    )
                # 删除临时文件
                os.remove(temp_file_path)
                # 清除session中的临时文件信息
                del request.session['temp_resume_file']
                del request.session['temp_resume_filename']
            
            resume.save()
            form.save_m2m()  # 保存多对多关系
            messages.success(request, '简历创建成功！')
            return redirect('resume_detail', pk=resume.pk)
    else:
        form = ResumeForm()
    
    # 处理文件解析
    if request.method == 'POST' and 'parse_file' in request.POST and request.FILES.get('resume_file'):
        try:
            parser = ResumeParser()
            file = request.FILES['resume_file']
            
            # 保存文件到临时目录
            temp_dir = tempfile.gettempdir()
            temp_file_path = os.path.join(temp_dir, f'resume_{request.user.id}_{int(time.time())}')
            with open(temp_file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            
            # 将临时文件路径保存到session
            request.session['temp_resume_file'] = temp_file_path
            request.session['temp_resume_filename'] = file.name
            
            # 解析文件
            parsed_data = parser.parse_file(file)
            
            # 创建新的表单实例，预填充解析的数据
            form = ResumeForm(initial={
                'name': parsed_data.get('name', ''),
                'gender': parsed_data.get('gender', ''),
                'age': parsed_data.get('age', ''),
                'phone': parsed_data.get('phone', ''),
                'email': parsed_data.get('email', ''),
                'education': '\n'.join(parsed_data.get('education', [])),
                'work_experience': '\n'.join(parsed_data.get('work_experience', [])),
                'skills': '\n'.join(parsed_data.get('skills', [])),
            })
            
            messages.success(request, '文件解析成功！请检查并完善信息。')
        except Exception as e:
            messages.error(request, f'文件解析失败：{str(e)}')
            # 如果解析失败，删除临时文件
            if 'temp_resume_file' in request.session:
                temp_file_path = request.session['temp_resume_file']
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)
                del request.session['temp_resume_file']
                del request.session['temp_resume_filename']
    
    return render(request, 'headhunting/resume_form.html', {
        'form': form,
        'title': '创建简历'
    })

@login_required
def resume_detail(request, pk):
    """简历详情视图"""
    resume = get_object_or_404(Resume, pk=pk)
    
    # 检查权限
    if not request.user.is_system_admin and not request.user.is_admin and resume.created_by != request.user:
        return HttpResponseForbidden('您没有权限查看此简历')
    
    # 获取该简历的投递记录
    submissions = resume.project_submissions.all()
    
    # 获取可投递的项目（尚未投递的项目）
    submitted_project_ids = resume.project_submissions.values_list('project_id', flat=True)
    available_projects = Project.objects.exclude(id__in=submitted_project_ids).filter(status__code='active')
    
    # 获取可用标签（已有的标签）
    current_tag_ids = resume.tags.values_list('id', flat=True)
    available_tags = Tag.objects.exclude(id__in=current_tag_ids)
    if not request.user.is_system_admin:
        available_tags = available_tags.filter(Q(created_by=request.user) | Q(created_by__isnull=True))
    
    # 检查当前用户是否已收藏该简历
    is_bookmarked = ResumeBookmark.objects.filter(resume=resume, user=request.user).exists()
    
    return render(request, 'headhunting/resume_detail.html', {
        'resume': resume,
        'submissions': submissions,
        'projects': available_projects,
        'available_tags': available_tags,
        'is_bookmarked': is_bookmarked
    })

@login_required
def resume_update(request, pk):
    """更新简历视图"""
    resume = get_object_or_404(Resume, pk=pk)
    
    # 检查权限
    if not request.user.is_system_admin and not request.user.is_admin and resume.created_by != request.user:
        return HttpResponseForbidden('您没有权限编辑此简历')
    
    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES, instance=resume)
        if form.is_valid():
            form.save()
            messages.success(request, '简历更新成功')
            return redirect('resume_detail', pk=resume.pk)
    else:
        form = ResumeForm(instance=resume)
    
    return render(request, 'headhunting/resume_form.html', {'form': form, 'title': f'编辑简历: {resume.name}'})

@login_required
def resume_delete(request, pk):
    """删除简历视图"""
    resume = get_object_or_404(Resume, pk=pk)
    
    # 检查权限
    if not request.user.is_system_admin and not request.user.is_admin and resume.created_by != request.user:
        return HttpResponseForbidden('您没有权限删除此简历')
    
    if request.method == 'POST':
        resume.delete()
        messages.success(request, '简历删除成功')
        return redirect('resume_list')
    
    return render(request, 'headhunting/resume_confirm_delete.html', {'resume': resume})

@login_required
def resume_add_tag(request, pk):
    """添加标签到简历视图"""
    resume = get_object_or_404(Resume, pk=pk)
    
    # 检查权限
    if not request.user.is_system_admin and not request.user.is_admin and resume.created_by != request.user:
        return HttpResponseForbidden('您没有权限为此简历添加标签')
    
    if request.method == 'POST':
        tag_id = request.POST.get('tag_id')
        new_tag_name = request.POST.get('new_tag_name')
        tag_color = request.POST.get('tag_color', '#0d6efd')
        
        if tag_id:
            # 使用现有标签
            tag = get_object_or_404(Tag, pk=tag_id)
            resume.tags.add(tag)
            messages.success(request, f'标签 "{tag.name}" 已添加到简历')
        elif new_tag_name:
            # 创建新标签
            tag, created = Tag.objects.get_or_create(
                name=new_tag_name,
                defaults={'color': tag_color, 'created_by': request.user}
            )
            resume.tags.add(tag)
            if created:
                messages.success(request, f'新标签 "{tag.name}" 已创建并添加到简历')
            else:
                messages.success(request, f'标签 "{tag.name}" 已添加到简历')
        else:
            messages.error(request, '请选择或创建标签')
        
        return redirect('resume_detail', pk=resume.pk)
    
    return redirect('resume_detail', pk=resume.pk)

# 简历投递管理
@login_required
def resume_submit(request, resume_id, project_id):
    """简历投递视图"""
    resume = get_object_or_404(Resume, pk=resume_id)
    project = get_object_or_404(Project, pk=project_id)
    
    # 检查权限
    if not request.user.is_system_admin and not request.user.is_admin and resume.created_by != request.user:
        return HttpResponseForbidden('您没有权限操作此简历')
    
    # 检查是否已投递
    if ResumeProject.objects.filter(resume=resume, project=project).exists():
        messages.error(request, '该简历已经投递到此项目')
        return redirect('resume_detail', pk=resume_id)
    
    if request.method == 'POST':
        form = ResumeSubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.resume = resume
            submission.project = project
            submission.save()
            messages.success(request, '简历投递成功')
            return redirect('resume_detail', pk=resume_id)
    else:
        form = ResumeSubmissionForm()
    
    return render(request, 'headhunting/resume_submit.html', {
        'form': form,
        'resume': resume,
        'project': project
    })

@admin_required
def submission_update_status(request, pk):
    """更新投递状态视图 - 需要管理员权限"""
    submission = get_object_or_404(ResumeProject, pk=pk)
    
    # 检查权限
    if not request.user.is_system_admin and submission.project.created_by != request.user:
        return HttpResponseForbidden('您没有权限更新此投递状态')
    
    # 获取来源参数，用于返回按钮
    from_project = request.GET.get('from_project', 'true').lower() == 'true'
    
    if request.method == 'POST':
        form = SubmissionStatusForm(request.POST, instance=submission)
        if form.is_valid():
            form.save()
            messages.success(request, '投递状态更新成功')
            # 根据来源决定重定向目标
            if from_project:
                return redirect('project_detail', pk=submission.project.pk)
            else:
                return redirect('resume_detail', pk=submission.resume.pk)
    else:
        form = SubmissionStatusForm(instance=submission)
    
    return render(request, 'headhunting/submission_status_form.html', {
        'form': form,
        'submission': submission,
        'from_project': from_project
    })

# 标签管理视图
@login_required
def tag_list(request):
    """标签列表视图"""
    tags = Tag.objects.all()
    
    # 非系统管理员只能看到自己创建的标签和公共标签
    if not request.user.is_system_admin:
        tags = tags.filter(Q(created_by=request.user) | Q(created_by__isnull=True))
    
    # 搜索功能
    query = request.GET.get('q')
    if query:
        tags = tags.filter(name__icontains=query)
    
    return render(request, 'headhunting/tag_list.html', {'tags': tags})

@login_required
def tag_create(request):
    """创建标签视图"""
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.created_by = request.user
            tag.save()
            messages.success(request, '标签创建成功')
            return redirect('tag_list')
    else:
        form = TagForm()
    
    return render(request, 'headhunting/tag_form.html', {'form': form, 'title': '创建标签'})

@login_required
def tag_update(request, pk):
    """更新标签视图"""
    tag = get_object_or_404(Tag, pk=pk)
    
    # 检查权限
    if not request.user.is_system_admin and tag.created_by != request.user:
        return HttpResponseForbidden('您没有权限编辑此标签')
    
    if request.method == 'POST':
        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            messages.success(request, '标签更新成功')
            return redirect('tag_list')
    else:
        form = TagForm(instance=tag)
    
    return render(request, 'headhunting/tag_form.html', {'form': form, 'title': f'编辑标签: {tag.name}'})

@login_required
def tag_delete(request, pk):
    """删除标签视图"""
    tag = get_object_or_404(Tag, pk=pk)
    
    # 检查权限
    if not request.user.is_system_admin and tag.created_by != request.user:
        return HttpResponseForbidden('您没有权限删除此标签')
    
    if request.method == 'POST':
        tag.delete()
        messages.success(request, '标签删除成功')
        return redirect('tag_list')
    
    return render(request, 'headhunting/tag_confirm_delete.html', {'tag': tag})

# 状态管理视图
@admin_required
def project_status_list(request):
    """项目状态列表视图"""
    statuses = ProjectStatus.objects.all()
    
    # 搜索功能
    query = request.GET.get('q')
    if query:
        statuses = statuses.filter(Q(name__icontains=query) | Q(code__icontains=query))
    
    return render(request, 'headhunting/project_status_list.html', {'statuses': statuses})

@admin_required
def project_status_create(request):
    """创建项目状态视图"""
    if request.method == 'POST':
        form = ProjectStatusForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '项目状态创建成功')
            return redirect('project_status_list')
    else:
        form = ProjectStatusForm()
    
    return render(request, 'headhunting/status_form.html', {
        'form': form, 
        'title': '创建项目状态',
        'status_type': 'project'
    })

@admin_required
def project_status_update(request, pk):
    """更新项目状态视图"""
    status = get_object_or_404(ProjectStatus, pk=pk)
    
    if request.method == 'POST':
        form = ProjectStatusForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            messages.success(request, '项目状态更新成功')
            return redirect('project_status_list')
    else:
        form = ProjectStatusForm(instance=status)
    
    return render(request, 'headhunting/status_form.html', {
        'form': form, 
        'title': f'编辑项目状态: {status.name}',
        'status_type': 'project'
    })

@admin_required
def project_status_delete(request, pk):
    """删除项目状态视图"""
    status = get_object_or_404(ProjectStatus, pk=pk)
    
    # 检查是否有项目使用此状态
    projects_count = Project.objects.filter(status=status).count()
    if projects_count > 0 and request.method != 'POST':
        messages.warning(request, f'有{projects_count}个项目正在使用此状态，删除可能导致数据错误')
    
    if request.method == 'POST':
        status.delete()
        messages.success(request, '项目状态删除成功')
        return redirect('project_status_list')
    
    return render(request, 'headhunting/status_confirm_delete.html', {
        'status': status,
        'status_type': 'project'
    })

@admin_required
def resume_status_list(request):
    """简历状态列表视图"""
    statuses = ResumeStatus.objects.all()
    
    # 搜索功能
    query = request.GET.get('q')
    if query:
        statuses = statuses.filter(Q(name__icontains=query) | Q(code__icontains=query))
    
    return render(request, 'headhunting/resume_status_list.html', {'statuses': statuses})

@admin_required
def resume_status_create(request):
    """创建简历状态视图"""
    if request.method == 'POST':
        form = ResumeStatusForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '简历状态创建成功')
            return redirect('resume_status_list')
    else:
        form = ResumeStatusForm()
    
    return render(request, 'headhunting/status_form.html', {
        'form': form, 
        'title': '创建简历状态',
        'status_type': 'resume'
    })

@admin_required
def resume_status_update(request, pk):
    """更新简历状态视图"""
    status = get_object_or_404(ResumeStatus, pk=pk)
    
    if request.method == 'POST':
        form = ResumeStatusForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            messages.success(request, '简历状态更新成功')
            return redirect('resume_status_list')
    else:
        form = ResumeStatusForm(instance=status)
    
    return render(request, 'headhunting/status_form.html', {
        'form': form, 
        'title': f'编辑简历状态: {status.name}',
        'status_type': 'resume'
    })

@admin_required
def resume_status_delete(request, pk):
    """删除简历状态视图"""
    status = get_object_or_404(ResumeStatus, pk=pk)
    
    # 检查是否有简历投递记录使用此状态
    submissions_count = ResumeProject.objects.filter(status=status).count()
    if submissions_count > 0 and request.method != 'POST':
        messages.warning(request, f'有{submissions_count}条简历投递记录正在使用此状态，删除可能导致数据错误')
    
    if request.method == 'POST':
        status.delete()
        messages.success(request, '简历状态删除成功')
        return redirect('resume_status_list')
    
    return render(request, 'headhunting/status_confirm_delete.html', {
        'status': status,
        'status_type': 'resume'
    })

# 回款记录管理视图
@admin_required
def payment_list(request, project_id):
    """项目回款记录列表视图"""
    project = get_object_or_404(Project, pk=project_id)
    
    # 检查权限
    if not request.user.is_system_admin and project.created_by != request.user:
        return HttpResponseForbidden('您没有权限查看此项目的回款记录')
    
    payments = project.payment_records.all()
    
    # 计算总金额
    total_amount = payments.aggregate(total=Sum('amount'))['total'] or 0
    
    return render(request, 'headhunting/payment_list.html', {
        'project': project,
        'payments': payments,
        'total_amount': total_amount
    })

@admin_required
def payment_create(request, project_id):
    """创建回款记录视图"""
    project = get_object_or_404(Project, pk=project_id)
    
    # 检查权限
    if not request.user.is_system_admin and project.created_by != request.user:
        return HttpResponseForbidden('您没有权限为此项目添加回款记录')
    
    if request.method == 'POST':
        form = PaymentRecordForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.project = project
            payment.created_by = request.user
            payment.save()
            messages.success(request, '回款记录添加成功')
            return redirect('payment_list', project_id=project.id)
    else:
        form = PaymentRecordForm()
    
    return render(request, 'headhunting/payment_form.html', {
        'form': form,
        'title': f'添加回款记录: {project.title}',
        'project': project
    })

@admin_required
def payment_update(request, pk):
    """更新回款记录视图"""
    payment = get_object_or_404(PaymentRecord, pk=pk)
    project = payment.project
    
    # 检查权限
    if not request.user.is_system_admin and payment.created_by != request.user:
        return HttpResponseForbidden('您没有权限编辑此回款记录')
    
    if request.method == 'POST':
        form = PaymentRecordForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            messages.success(request, '回款记录更新成功')
            return redirect('payment_list', project_id=project.id)
    else:
        form = PaymentRecordForm(instance=payment)
    
    return render(request, 'headhunting/payment_form.html', {
        'form': form,
        'title': f'编辑回款记录: {project.title}',
        'project': project
    })

@admin_required
def payment_delete(request, pk):
    """删除回款记录视图"""
    payment = get_object_or_404(PaymentRecord, pk=pk)
    project = payment.project
    
    # 检查权限
    if not request.user.is_system_admin and payment.created_by != request.user:
        return HttpResponseForbidden('您没有权限删除此回款记录')
    
    if request.method == 'POST':
        payment.delete()
        messages.success(request, '回款记录删除成功')
        return redirect('payment_list', project_id=project.id)
    
    return render(request, 'headhunting/payment_confirm_delete.html', {'payment': payment})

# 简历收藏管理
@login_required
def resume_bookmark_toggle(request, pk):
    """收藏/取消收藏简历"""
    resume = get_object_or_404(Resume, pk=pk)
    
    # 检查权限
    if not request.user.is_system_admin and not request.user.is_admin and resume.created_by != request.user:
        return HttpResponseForbidden('您没有权限收藏此简历')
    
    # 检查是否已收藏
    bookmark, created = ResumeBookmark.objects.get_or_create(
        resume=resume,
        user=request.user
    )
    
    # 如果已存在则删除（取消收藏）
    if not created:
        bookmark.delete()
        is_bookmarked = False
        message = '已取消收藏'
    else:
        is_bookmarked = True
        message = '已加入收藏'
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'is_bookmarked': is_bookmarked,
            'message': message
        })
    else:
        messages.success(request, message)
        return redirect('resume_detail', pk=pk)

@login_required
def resume_bookmark_list(request):
    """收藏的简历列表视图"""
    # 获取当前用户收藏的所有简历
    bookmarks = ResumeBookmark.objects.filter(user=request.user).select_related('resume')
    
    # 获取活跃的项目供投递使用
    projects = Project.objects.filter(status__code='active')
    
    return render(request, 'headhunting/resume_bookmark_list.html', {
        'bookmarks': bookmarks,
        'projects': projects
    })

# 仪表板视图
@login_required
def hr_dashboard(request):
    """HR仪表板视图"""
    context = {}
    
    # 获取公司统计 - 所有用户都能看到全部统计
    companies_count = Company.objects.count()
    
    # 获取项目统计 - 所有用户都能看到全部统计
    projects = Project.objects.all()
    projects_count = projects.count()
    
    # 获取简历统计 - 所有用户都能看到全部统计
    resumes = Resume.objects.all()
    resumes_count = resumes.count()
    
    # 获取项目状态统计
    project_status_stats = projects.values('status__name').annotate(count=Count('id')).order_by('-count')
    
    # 获取简历状态统计
    resume_submissions = ResumeProject.objects.filter(project__in=projects)
    resume_status_stats = resume_submissions.values('status__name').annotate(count=Count('id')).order_by('-count')
    
    # 计算简历状态总数
    resume_status_total = resume_submissions.count()
    
    # 获取回款统计
    total_payment = PaymentRecord.objects.filter(project__in=projects).aggregate(total=Sum('amount'))['total'] or 0
    
    # 获取最近活动
    recent_activities = []
    
    # 最近新增的公司
    recent_companies = Company.objects.all().order_by('-created_at')[:5]
    
    for company in recent_companies:
        recent_activities.append({
            'type': 'company',
            'action': '新增公司',
            'object': company,
            'time': company.created_at,
            'url': reverse('company_detail', args=[company.id])
        })
    
    # 最近新增的项目
    recent_projects = Project.objects.all().order_by('-created_at')[:5]
    
    for project in recent_projects:
        recent_activities.append({
            'type': 'project',
            'action': '新增项目',
            'object': project,
            'time': project.created_at,
            'url': reverse('project_detail', args=[project.id])
        })
    
    # 最近新增的简历
    recent_resumes = Resume.objects.all().order_by('-created_at')[:5]
    
    for resume in recent_resumes:
        recent_activities.append({
            'type': 'resume',
            'action': '新增简历',
            'object': resume,
            'time': resume.created_at,
            'url': reverse('resume_detail', args=[resume.id])
        })
    
    # 最近的投递记录
    recent_submissions = ResumeProject.objects.all().order_by('-submitted_at')[:5]
    
    for submission in recent_submissions:
        recent_activities.append({
            'type': 'submission',
            'action': '简历投递',
            'object': submission,
            'time': submission.submitted_at,
            'url': reverse('project_detail', args=[submission.project.id])
        })
    
    # 最近的回款记录
    recent_payments = PaymentRecord.objects.all().order_by('-created_at')[:5]
    
    for payment in recent_payments:
        recent_activities.append({
            'type': 'payment',
            'action': '回款记录',
            'object': payment,
            'time': payment.created_at,
            'url': reverse('payment_list', args=[payment.project.id])
        })
    
    # 按时间排序所有活动
    recent_activities.sort(key=lambda x: x['time'], reverse=True)
    recent_activities = recent_activities[:10]  # 只显示最近10条
    
    # 获取简历收藏数量
    bookmarks_count = 0
    if request.user.is_authenticated:
        bookmarks_count = ResumeBookmark.objects.filter(user=request.user).count()
    
    context = {
        'companies_count': companies_count,
        'projects_count': projects_count,
        'resumes_count': resumes_count,
        'bookmarks_count': bookmarks_count,
        'project_status_stats': project_status_stats,
        'resume_status_stats': resume_status_stats,
        'resume_status_total': resume_status_total,
        'total_payment': total_payment,
        'recent_activities': recent_activities
    }
    
    return render(request, 'headhunting/dashboard.html', context)

@login_required
def resume_download(request, pk):
    """下载简历文件"""
    resume = get_object_or_404(Resume, pk=pk)
    
    # 检查权限
    if not request.user.is_system_admin and not request.user.is_admin and resume.created_by != request.user:
        return HttpResponseForbidden('您没有权限下载此简历')
    
    if resume.resume_file:
        file_path = resume.resume_file.path
        if os.path.exists(file_path):
            # 获取文件类型
            content_type, _ = mimetypes.guess_type(file_path)
            if not content_type:
                content_type = 'application/octet-stream'
            
            # 打开文件
            file = open(file_path, 'rb')
            response = FileResponse(file, content_type=content_type)
            
            # 设置文件名
            filename = os.path.basename(file_path)
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            
            return response
    
    messages.error(request, '文件不存在')
    return redirect('resume_detail', pk=pk)

@login_required
def resume_preview(request, pk):
    """在线预览简历文件"""
    resume = get_object_or_404(Resume, pk=pk)
    
    # 检查权限
    if not request.user.is_system_admin and not request.user.is_admin and resume.created_by != request.user:
        return HttpResponseForbidden('您没有权限预览此简历')
    
    if resume.resume_file:
        file_path = resume.resume_file.path
        if os.path.exists(file_path):
            # 获取文件类型
            content_type, _ = mimetypes.guess_type(file_path)
            if not content_type:
                content_type = 'application/octet-stream'
            
            # 对于PDF文件，直接返回
            if content_type == 'application/pdf':
                file = open(file_path, 'rb')
                response = FileResponse(file, content_type=content_type)
                response['Content-Disposition'] = 'inline'
                return response
            
            # 对于Word文件，返回提示信息
            elif content_type in ['application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
                messages.warning(request, 'Word文件暂不支持在线预览，请下载后查看')
                return redirect('resume_detail', pk=pk)
    
    messages.error(request, '文件不存在')
    return redirect('resume_detail', pk=pk)
