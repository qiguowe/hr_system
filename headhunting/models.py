from django.db import models
from accounts.models import User

class StatusOption(models.Model):
    """状态选项基础模型"""
    name = models.CharField(max_length=50, verbose_name='状态名称')
    code = models.CharField(max_length=50, unique=True, verbose_name='状态代码')
    description = models.TextField(blank=True, null=True, verbose_name='描述')
    order = models.IntegerField(default=0, verbose_name='排序')
    is_active = models.BooleanField(default=True, verbose_name='是否激活')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        abstract = True
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return self.name

class ProjectStatus(StatusOption):
    """项目状态模型"""
    class Meta:
        verbose_name = '项目状态'
        verbose_name_plural = verbose_name

class ResumeStatus(StatusOption):
    """简历状态模型"""
    class Meta:
        verbose_name = '简历状态'
        verbose_name_plural = verbose_name

class Tag(models.Model):
    """标签模型"""
    name = models.CharField(max_length=50, unique=True, verbose_name='标签名称')
    color = models.CharField(max_length=20, default='#28a745', verbose_name='标签颜色')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_tags', verbose_name='创建人')
    
    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Company(models.Model):
    """对接公司模型"""
    name = models.CharField(max_length=100, verbose_name='公司名称')
    address = models.CharField(max_length=200, blank=True, null=True, verbose_name='地址')
    contact_person = models.CharField(max_length=50, blank=True, null=True, verbose_name='联系人')
    contact_phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='联系电话')
    contact_email = models.EmailField(blank=True, null=True, verbose_name='联系邮箱')
    description = models.TextField(blank=True, null=True, verbose_name='公司描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_companies', verbose_name='创建人')
    
    class Meta:
        verbose_name = '公司'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name

class Project(models.Model):
    """招聘项目模型"""
    title = models.CharField(max_length=100, verbose_name='项目标题')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='projects', verbose_name='关联公司')
    job_title = models.CharField(max_length=100, verbose_name='职位名称')
    job_description = models.TextField(verbose_name='职位描述')
    requirements = models.TextField(verbose_name='职位要求')
    salary_range = models.CharField(max_length=50, blank=True, null=True, verbose_name='薪资范围')
    location = models.CharField(max_length=100, blank=True, null=True, verbose_name='工作地点')
    status = models.ForeignKey(ProjectStatus, on_delete=models.SET_NULL, null=True, verbose_name='项目状态')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    deadline = models.DateField(blank=True, null=True, verbose_name='截止日期')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_projects', verbose_name='创建人')
    
    class Meta:
        verbose_name = '项目'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title

class PaymentRecord(models.Model):
    """项目回款记录模型"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='payment_records', verbose_name='关联项目')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='回款金额')
    payment_date = models.DateField(verbose_name='回款日期')
    description = models.TextField(blank=True, null=True, verbose_name='回款说明')
    payment_method = models.CharField(max_length=50, blank=True, null=True, verbose_name='付款方式')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_payments', verbose_name='创建人')
    
    class Meta:
        verbose_name = '回款记录'
        verbose_name_plural = verbose_name
        ordering = ['-payment_date']
    
    def __str__(self):
        return f"{self.project.title} - {self.amount}元"

class Resume(models.Model):
    """简历模型"""
    GENDER_CHOICES = [
        ('male', '男'),
        ('female', '女'),
        ('other', '其他'),
    ]
    
    EDUCATION_CHOICES = [
        ('high_school', '高中'),
        ('college', '大专'),
        ('bachelor', '本科'),
        ('master', '硕士'),
        ('phd', '博士'),
        ('other', '其他'),
    ]
    
    name = models.CharField(max_length=50, verbose_name='姓名')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name='性别')
    birth_date = models.DateField(blank=True, null=True, verbose_name='出生日期')
    phone = models.CharField(max_length=20, verbose_name='电话')
    email = models.EmailField(verbose_name='邮箱')
    education = models.CharField(max_length=20, choices=EDUCATION_CHOICES, verbose_name='最高学历')
    school = models.CharField(max_length=100, blank=True, null=True, verbose_name='毕业院校')
    major = models.CharField(max_length=100, blank=True, null=True, verbose_name='专业')
    experience_years = models.IntegerField(default=0, verbose_name='工作年限')
    current_company = models.CharField(max_length=100, blank=True, null=True, verbose_name='当前公司')
    current_position = models.CharField(max_length=100, blank=True, null=True, verbose_name='当前职位')
    skills = models.TextField(blank=True, null=True, verbose_name='技能')
    work_experience = models.TextField(blank=True, null=True, verbose_name='工作经历')
    work_exp_1_company = models.CharField(max_length=100, null=True, blank=True, verbose_name='公司1')
    work_exp_1_position = models.CharField(max_length=100, null=True, blank=True, verbose_name='职位1')
    work_exp_1_period = models.CharField(max_length=100, null=True, blank=True, verbose_name='时间段1')
    work_exp_1_description = models.TextField(null=True, blank=True, verbose_name='工作描述1')
    work_exp_2_company = models.CharField(max_length=100, null=True, blank=True, verbose_name='公司2')
    work_exp_2_position = models.CharField(max_length=100, null=True, blank=True, verbose_name='职位2')
    work_exp_2_period = models.CharField(max_length=100, null=True, blank=True, verbose_name='时间段2')
    work_exp_2_description = models.TextField(null=True, blank=True, verbose_name='工作描述2')
    work_exp_3_company = models.CharField(max_length=100, null=True, blank=True, verbose_name='公司3')
    work_exp_3_position = models.CharField(max_length=100, null=True, blank=True, verbose_name='职位3')
    work_exp_3_period = models.CharField(max_length=100, null=True, blank=True, verbose_name='时间段3')
    work_exp_3_description = models.TextField(null=True, blank=True, verbose_name='工作描述3')
    tags = models.ManyToManyField(Tag, blank=True, related_name='resumes', verbose_name='标签')
    resume_file = models.FileField(upload_to='resume_files/', null=True, blank=True, verbose_name='简历文件')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_resumes', verbose_name='创建人')
    
    class Meta:
        verbose_name = '简历'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name

class ResumeProject(models.Model):
    """简历项目关联模型，记录简历投递到项目的情况"""
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='project_submissions', verbose_name='简历')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='resume_submissions', verbose_name='项目')
    status = models.ForeignKey(ResumeStatus, on_delete=models.SET_NULL, null=True, verbose_name='状态')
    notes = models.TextField(blank=True, null=True, verbose_name='备注')
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name='投递时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '简历投递记录'
        verbose_name_plural = verbose_name
        ordering = ['-submitted_at']
        unique_together = ['resume', 'project']  # 同一个简历不能重复投递同一个项目
    
    def __str__(self):
        return f"{self.resume.name} - {self.project.title}"

class ResumeBookmark(models.Model):
    """简历收藏模型"""
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='bookmarks', verbose_name='简历')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resume_bookmarks', verbose_name='用户')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='收藏时间')
    
    class Meta:
        verbose_name = '简历收藏'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
        unique_together = ['resume', 'user']  # 同一用户不能重复收藏同一简历
    
    def __str__(self):
        return f"{self.user.username} - {self.resume.name}"
