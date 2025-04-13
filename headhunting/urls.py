from django.urls import path
from . import views

urlpatterns = [
    # 公司管理
    path('companies/', views.company_list, name='company_list'),
    path('companies/create/', views.company_create, name='company_create'),
    path('companies/<int:pk>/', views.company_detail, name='company_detail'),
    path('companies/<int:pk>/update/', views.company_update, name='company_update'),
    path('companies/<int:pk>/delete/', views.company_delete, name='company_delete'),
    
    # 项目管理
    path('projects/', views.project_list, name='project_list'),
    path('projects/create/', views.project_create, name='project_create'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('projects/<int:pk>/update/', views.project_update, name='project_update'),
    path('projects/<int:pk>/delete/', views.project_delete, name='project_delete'),
    
    # 项目回款记录
    path('projects/<int:project_id>/payments/', views.payment_list, name='payment_list'),
    path('projects/<int:project_id>/payments/create/', views.payment_create, name='payment_create'),
    path('payments/<int:pk>/update/', views.payment_update, name='payment_update'),
    path('payments/<int:pk>/delete/', views.payment_delete, name='payment_delete'),
    
    # 简历管理
    path('resumes/', views.resume_list, name='resume_list'),
    path('resumes/create/', views.resume_create, name='resume_create'),
    path('resumes/<int:pk>/', views.resume_detail, name='resume_detail'),
    path('resumes/<int:pk>/update/', views.resume_update, name='resume_update'),
    path('resumes/<int:pk>/delete/', views.resume_delete, name='resume_delete'),
    path('resumes/<int:pk>/add-tag/', views.resume_add_tag, name='resume_add_tag'),
    path('resumes/<int:pk>/bookmark/', views.resume_bookmark_toggle, name='resume_bookmark_toggle'),
    path('bookmarks/', views.resume_bookmark_list, name='resume_bookmark_list'),
    
    # 简历投递
    path('resumes/<int:resume_id>/submit/<int:project_id>/', views.resume_submit, name='resume_submit'),
    path('submissions/<int:pk>/update_status/', views.submission_update_status, name='submission_update_status'),
    
    # 标签管理
    path('tags/', views.tag_list, name='tag_list'),
    path('tags/create/', views.tag_create, name='tag_create'),
    path('tags/<int:pk>/update/', views.tag_update, name='tag_update'),
    path('tags/<int:pk>/delete/', views.tag_delete, name='tag_delete'),
    
    # 状态管理
    path('project-statuses/', views.project_status_list, name='project_status_list'),
    path('project-statuses/create/', views.project_status_create, name='project_status_create'),
    path('project-statuses/<int:pk>/update/', views.project_status_update, name='project_status_update'),
    path('project-statuses/<int:pk>/delete/', views.project_status_delete, name='project_status_delete'),
    
    path('resume-statuses/', views.resume_status_list, name='resume_status_list'),
    path('resume-statuses/create/', views.resume_status_create, name='resume_status_create'),
    path('resume-statuses/<int:pk>/update/', views.resume_status_update, name='resume_status_update'),
    path('resume-statuses/<int:pk>/delete/', views.resume_status_delete, name='resume_status_delete'),
    
    # 仪表板
    path('dashboard/', views.hr_dashboard, name='hr_dashboard'),
] 