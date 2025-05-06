# 猎头管理系统

猎头管理系统是一个基于Django开发的综合性人才招聘管理平台，专为猎头公司设计，提供公司管理、项目跟踪、简历收集、人才推荐和回款统计等核心功能。本系统帮助猎头顾问高效管理招聘流程，提升工作效率。

## 功能特点

- **公司管理**：管理客户公司信息，包括基本信息、联系人等
- **项目管理**：跟踪招聘项目进度，管理职位需求
- **简历管理**：
  - 支持PDF和Word格式简历上传
  - 自动解析简历信息
  - 简历分类和标签管理
  - 简历收藏功能
- **人才推荐**：
  - 简历投递管理
  - 面试流程跟踪
  - 候选人状态更新
- **回款管理**：
  - 回款记录管理
  - 试用期跟踪
  - 回款统计
- **数据统计**：
  - 项目状态统计
  - 简历状态统计
  - 回款金额统计
  - 最近活动记录

## 技术栈

- **后端**：Django 4.2
- **前端**：
  - Bootstrap 5
  - jQuery
  - Select2
  - Animate.css
- **数据库**：SQLite（可配置为其他数据库）
- **其他**：
  - django-crispy-forms
  - crispy-bootstrap5
  - python-docx
  - PyPDF2
  - spaCy（中文NLP）

## 安装说明

1. 克隆仓库：
```bash
git clone https://github.com/qiguowe/hr_system.git
cd hr_system
```

2. 创建虚拟环境：
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 安装中文语言模型：
```bash
python -m spacy download zh_core_web_sm
```

5. 初始化数据库：
```bash
python manage.py makemigrations
python manage.py migrate
```

6. 创建超级用户：
```bash
python manage.py createsuperuser
```

7. 运行开发服务器：
```bash
python manage.py runserver
```

## 测试账号

- 邮箱：qgw1@outlook.com
- 密码：admin123

## 使用说明

1. 访问系统：http://localhost:8000
2. 使用测试账号登录系统
3. 开始使用各项功能：
   - 创建和管理公司信息
   - 创建招聘项目
   - 上传和解析简历
   - 管理简历投递
   - 跟踪回款记录

## 开发说明

1. 代码规范：
   - 遵循PEP 8规范
   - 使用4个空格缩进
   - 类名使用驼峰命名
   - 函数和变量使用下划线命名

2. 提交规范：
   - feat: 新功能
   - fix: 修复bug
   - docs: 文档更新
   - style: 代码格式调整
   - refactor: 代码重构
   - test: 测试用例
   - chore: 其他修改

## 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 贡献指南

1. Fork 本仓库
2. 创建特性分支：`git checkout -b feature/your-feature`
3. 提交更改：`git commit -m 'feat: add some feature'`
4. 推送到分支：`git push origin feature/your-feature`
5. 提交 Pull Request

## 联系方式

如有问题或建议，请通过以下方式联系：

- 邮箱：qgw1@outlook.com
- GitHub Issues：[提交问题](https://github.com/qiguowe/hr_system/issues)

## 功能概览

### 核心功能

1. **公司管理**
   - 创建和管理合作客户公司信息
   - 记录公司联系人、地址等详细信息
   - 查看公司相关的招聘项目

2. **项目管理**
   - 创建和跟踪招聘项目
   - 设置项目状态（活跃、暂停、完成等）
   - 记录职位描述、要求、薪资范围等详情
   - 关联项目与公司

3. **简历管理**
   - 创建和维护候选人简历库
   - 支持添加工作经历、教育背景、技能等完整信息
   - 简历标签系统，便于分类和检索
   - 支持简历文件上传和下载
   - 收藏重要简历功能

4. **投递管理**
   - 将简历投递到特定项目
   - 追踪投递状态（已提交、审核中、面试中、已发offer、已拒绝等）
   - 记录每次状态更新的备注信息

5. **回款管理**
   - 记录项目回款情况
   - 统计回款金额和项目收益
   - 支持多次回款记录

6. **数据统计**
   - 仪表板显示关键数据指标
   - 项目状态和简历投递状态统计
   - 最近活动时间线展示
   - 回款统计分析

### 用户权限管理

系统支持三级权限管理：

1. **普通用户**
   - 可以查看所有公司和项目
   - 可以创建新的公司和项目
   - 只能查看和管理自己创建的简历
   - 可以投递自己的简历到项目

2. **普通管理员**
   - 具备普通用户的所有权限
   - 可以编辑和删除所有公司和项目
   - 可以查看和管理所有简历
   - 可以更新所有投递状态

3. **系统管理员**
   - 拥有系统的最高权限
   - 可以管理用户账户
   - 可以管理系统配置

## 数据模型

系统主要包含以下数据模型：

1. **公司 (Company)**
   - 公司名称、地址、联系人等基本信息
   - 创建时间、创建人等元数据

2. **项目 (Project)**
   - 标题、关联公司、职位名称等基本信息
   - 职位描述、要求、薪资范围等详情
   - 项目状态、截止日期等管理信息
   - 创建时间、创建人等元数据

3. **简历 (Resume)**
   - 基本信息：姓名、性别、联系方式等
   - 教育背景：学历、学校、专业
   - 工作情况：工作年限、当前公司和职位
   - 工作经历：详细的工作经历记录
   - 技能、标签等附加信息
   - 简历文件、创建信息等元数据

4. **简历投递 (ResumeProject)**
   - 关联简历和项目
   - 投递状态、备注
   - 投递时间、更新时间等元数据

5. **回款记录 (PaymentRecord)**
   - 关联项目
   - 金额、日期、付款方式
   - 备注说明、创建信息等元数据

6. **标签 (Tag)**
   - 名称、颜色
   - 创建人、创建时间

7. **状态选项 (StatusOption)**
   - 项目状态 (ProjectStatus)
   - 简历状态 (ResumeStatus)

8. **简历收藏 (ResumeBookmark)**
   - 关联简历和用户
   - 收藏时间

## 开发指南

### 目录结构

```
hr_system/
├── accounts/           # 用户账户相关模块
├── headhunting/        # 核心业务逻辑模块
│   ├── migrations/     # 数据库迁移文件
│   ├── forms.py        # 表单定义
│   ├── models.py       # 数据模型定义
│   ├── urls.py         # URL路由配置
│   └── views.py        # 视图函数
├── templates/          # 模板文件
│   ├── accounts/       # 账户相关模板
│   ├── base/           # 基础模板
│   └── headhunting/    # 业务模板
├── static/             # 静态文件
├── media/              # 用户上传文件
├── hr_system/          # 项目配置
│   ├── settings.py     # 系统设置
│   ├── urls.py         # 主URL配置
│   └── wsgi.py         # WSGI配置
├── manage.py           # Django管理脚本
├── requirements.txt    # 依赖包列表
└── README.md           # 项目说明
```

### 扩展开发

如需扩展系统功能，可以考虑以下方向：

1. **导入/导出功能**：支持批量导入简历或导出数据
2. **高级搜索**：增加更复杂的搜索和筛选功能
3. **邮件通知**：添加邮件提醒功能
4. **API接口**：开发RESTful API供第三方集成
5. **数据可视化**：增强统计分析和图表展示
6. **候选人评估**：添加评分和评价功能

## 部署指南

### 生产环境部署

1. **服务器准备**
   - 推荐使用Linux服务器(Ubuntu/CentOS)
   - 安装Python 3.12+, Nginx, Gunicorn

2. **配置数据库**
   - 为生产环境配置MySQL或PostgreSQL
   - 修改settings.py中的数据库设置

3. **静态文件处理**
   - 收集静态文件：`python manage.py collectstatic`
   - 配置Nginx提供静态文件服务

4. **WSGI服务器配置**
   - 安装并配置Gunicorn
   - 创建systemd服务确保自动启动

5. **设置环境变量**
   - 敏感配置通过环境变量注入
   - 生产环境设置`DEBUG=False`

## 常见问题

1. **Q: 如何重置管理员密码?**  
   A: 使用命令`python manage.py changepassword <用户名>`

2. **Q: 如何备份数据?**  
   A: 使用命令`python manage.py dumpdata > backup.json`

3. **Q: 如何恢复数据?**  
   A: 使用命令`python manage.py loaddata backup.json`

4. **Q: 如何添加新的状态选项?**  
   A: 登录系统管理员账户，进入状态管理页面进行添加

## 致谢

感谢所有为本项目做出贡献的开发者，以及以下开源项目：

- Django
- Bootstrap 5
- Bootstrap Icons
- Animate.css 
