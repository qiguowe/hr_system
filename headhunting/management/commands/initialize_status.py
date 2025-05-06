from django.core.management.base import BaseCommand
from headhunting.models import ProjectStatus, ResumeStatus

class Command(BaseCommand):
    help = '初始化项目状态和简历状态数据'

    def handle(self, *args, **options):
        # 清空现有状态数据
        ProjectStatus.objects.all().delete()
        ResumeStatus.objects.all().delete()
        
        # 创建项目状态
        project_statuses = [
            {'name': '进行中', 'code': 'active', 'order': 1, 'description': '项目正在进行中'},
            {'name': '暂停', 'code': 'paused', 'order': 2, 'description': '项目暂时暂停'},
            {'name': '已完成', 'code': 'completed', 'order': 3, 'description': '项目已经完成'},
            {'name': '已取消', 'code': 'cancelled', 'order': 4, 'description': '项目已经取消'}
        ]
        
        for status_data in project_statuses:
            ProjectStatus.objects.create(**status_data)
            self.stdout.write(self.style.SUCCESS(f'创建项目状态: {status_data["name"]}'))
        
        # 创建简历状态
        resume_statuses = [
            {'name': '已投递', 'code': 'submitted', 'order': 1, 'description': '简历已经投递'},
            {'name': '审核中', 'code': 'reviewing', 'order': 2, 'description': '简历正在审核中'},
            {'name': '面试中', 'code': 'interview', 'order': 3, 'description': '候选人正在面试中'},
            {'name': '已录用', 'code': 'offer', 'order': 4, 'description': '候选人已录用'},
            {'name': '试用中', 'code': 'probation', 'order': 5, 'description': '候选人正在试用期'},
            {'name': '试用通过', 'code': 'probation_passed', 'order': 6, 'description': '候选人试用期已通过'},
            {'name': '已拒绝', 'code': 'rejected', 'order': 7, 'description': '候选人已被拒绝'},
            {'name': '已取消', 'code': 'cancelled', 'order': 8, 'description': '投递已被取消'}
        ]
        
        for status_data in resume_statuses:
            ResumeStatus.objects.create(**status_data)
            self.stdout.write(self.style.SUCCESS(f'创建简历状态: {status_data["name"]}'))
        
        self.stdout.write(self.style.SUCCESS('状态数据初始化完成!')) 