import os
import re
import logging
from datetime import datetime
from dateutil import parser
import spacy
from docx import Document
from PyPDF2 import PdfReader
from django.conf import settings

logger = logging.getLogger(__name__)

class ResumeParser:
    def __init__(self):
        try:
            # 加载中文语言模型
            self.nlp = spacy.load("zh_core_web_sm")
            logger.info("成功加载中文语言模型")
        except Exception as e:
            logger.error(f"加载中文语言模型失败: {str(e)}")
            raise
        
    def parse_file(self, file):
        """解析简历文件"""
        try:
            file_ext = os.path.splitext(file.name)[1].lower()
            logger.info(f"开始解析文件: {file.name}, 类型: {file_ext}")
            
            if file_ext == '.pdf':
                return self._parse_pdf(file)
            elif file_ext in ['.doc', '.docx']:
                return self._parse_docx(file)
            else:
                raise ValueError(f"不支持的文件格式: {file_ext}")
        except Exception as e:
            logger.error(f"解析文件失败: {str(e)}")
            raise
    
    def _parse_pdf(self, file):
        """解析PDF文件"""
        try:
            reader = PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            logger.info("PDF文件解析成功")
            return self._extract_info(self._preprocess_text(text))
        except Exception as e:
            logger.error(f"PDF解析失败: {str(e)}")
            raise
    
    def _parse_docx(self, file):
        """解析Word文件"""
        try:
            doc = Document(file)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            logger.info("Word文件解析成功")
            return self._extract_info(self._preprocess_text(text))
        except Exception as e:
            logger.error(f"Word解析失败: {str(e)}")
            raise
    
    def _preprocess_text(self, text):
        """预处理文本"""
        # 统一换行符
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        # 统一中文标点
        text = text.replace('：', ':').replace('，', ',').replace('、', ',')
        # 移除多余空白
        text = re.sub(r'\n\s*\n', '\n\n', text)
        # 移除特殊字符
        text = re.sub(r'[^\S\n]+', ' ', text)
        return text.strip()
    
    def _extract_info(self, text):
        """从文本中提取信息"""
        try:
            # 使用spaCy进行命名实体识别
            doc = self.nlp(text)
            
            # 提取基本信息
            info = {
                'name': self._extract_name(text),
                'gender': self._extract_gender(text),
                'age': self._extract_age(text),
                'phone': self._extract_phone(text),
                'email': self._extract_email(text),
                'education': self._extract_education(text),
                'work_experience': self._extract_work_experience(text),
                'skills': self._extract_skills(text),
            }
            
            logger.info("信息提取成功")
            return info
        except Exception as e:
            logger.error(f"信息提取失败: {str(e)}")
            raise
    
    def _extract_name(self, text):
        """提取姓名"""
        try:
            # 扩展姓名匹配模式
            name_patterns = [
                r'姓名[：:]\s*([^\n]+)',
                r'姓\s*名[：:]\s*([^\n]+)',
                r'([^\n]{2,4})\s*的简历',
                r'个人简历[：:]\s*([^\n]+)',
                r'([^\n]{2,4})\s*的个人简历',
            ]
            
            for pattern in name_patterns:
                match = re.search(pattern, text)
                if match:
                    name = match.group(1).strip()
                    # 清理可能的额外信息
                    name = re.sub(r'[（(].*?[)）]', '', name).strip()
                    if 2 <= len(name) <= 4:  # 中文姓名通常2-4个字
                        logger.info(f"提取到姓名: {name}")
                        return name
            
            # 使用spaCy的命名实体识别作为备选
            doc = self.nlp(text[:1000])  # 只分析前1000个字符
            for ent in doc.ents:
                if ent.label_ == 'PERSON' and 2 <= len(ent.text) <= 4:
                    logger.info(f"通过NER提取到姓名: {ent.text}")
                    return ent.text
            
            logger.warning("未找到姓名信息")
            return ""
        except Exception as e:
            logger.error(f"姓名提取失败: {str(e)}")
            return ""
    
    def _extract_gender(self, text):
        """提取性别"""
        try:
            gender_patterns = [
                r'性别[：:]\s*([男女])',
                r'([男女])\s*性',
                r'([男女])\s*生',
            ]
            
            for pattern in gender_patterns:
                match = re.search(pattern, text)
                if match:
                    gender = match.group(1)
                    logger.info(f"提取到性别: {gender}")
                    return gender
            
            logger.warning("未找到性别信息")
            return ""
        except Exception as e:
            logger.error(f"性别提取失败: {str(e)}")
            return ""
    
    def _extract_age(self, text):
        """提取年龄"""
        try:
            age_patterns = [
                r'年龄[：:]\s*(\d{1,2})',
                r'(\d{1,2})\s*岁',
                r'(\d{4})年出生',
            ]
            
            for pattern in age_patterns:
                match = re.search(pattern, text)
                if match:
                    if '年出生' in pattern:
                        birth_year = int(match.group(1))
                        age = datetime.now().year - birth_year
                    else:
                        age = int(match.group(1))
                    
                    if 18 <= age <= 65:  # 合理的年龄范围
                        logger.info(f"提取到年龄: {age}")
                        return str(age)
            
            logger.warning("未找到年龄信息")
            return ""
        except Exception as e:
            logger.error(f"年龄提取失败: {str(e)}")
            return ""
    
    def _extract_phone(self, text):
        """提取电话号码"""
        try:
            # 扩展电话号码匹配模式
            phone_patterns = [
                r'1[3-9]\d{9}',  # 标准手机号
                r'电话[：:]\s*1[3-9]\d{9}',
                r'手机[：:]\s*1[3-9]\d{9}',
                r'联系方式[：:]\s*1[3-9]\d{9}',
                r'联系电话[：:]\s*1[3-9]\d{9}',
                r'手机号码[：:]\s*1[3-9]\d{9}',
            ]
            
            for pattern in phone_patterns:
                match = re.search(pattern, text)
                if match:
                    phone = re.search(r'1[3-9]\d{9}', match.group(0)).group(0)
                    logger.info(f"提取到电话: {phone}")
                    return phone
            
            logger.warning("未找到电话号码")
            return ""
        except Exception as e:
            logger.error(f"电话提取失败: {str(e)}")
            return ""
    
    def _extract_email(self, text):
        """提取邮箱"""
        try:
            # 扩展邮箱匹配模式
            email_patterns = [
                r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',  # 标准邮箱
                r'邮箱[：:]\s*[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
                r'Email[：:]\s*[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
                r'电子邮箱[：:]\s*[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
                r'邮箱地址[：:]\s*[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            ]
            
            for pattern in email_patterns:
                match = re.search(pattern, text)
                if match:
                    email = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', match.group(0)).group(0)
                    logger.info(f"提取到邮箱: {email}")
                    return email
            
            logger.warning("未找到邮箱")
            return ""
        except Exception as e:
            logger.error(f"邮箱提取失败: {str(e)}")
            return ""
    
    def _extract_education(self, text):
        """提取教育经历"""
        try:
            education = []
            # 扩展教育经历匹配模式
            edu_patterns = [
                r'(?:教育背景|教育经历|学习经历|学历)[：:]\s*(.*?)(?=\n\n|\Z)',
                r'(?:教育背景|教育经历|学习经历|学历)\s*(.*?)(?=\n\n|\Z)',
            ]
            
            for pattern in edu_patterns:
                match = re.search(pattern, text, re.DOTALL)
                if match:
                    edu_text = match.group(1)
                    # 改进分割逻辑
                    edu_items = re.split(r'\n(?=\d{4}|\d{2}年)', edu_text)
                    for item in edu_items:
                        if item.strip():
                            # 清理和标准化教育经历
                            item = re.sub(r'\s+', ' ', item.strip())
                            if len(item) > 5:  # 过滤掉太短的条目
                                education.append(item)
                    if education:
                        logger.info(f"提取到{len(education)}条教育经历")
                        return education
            
            # 如果没有找到明确的教育经历标记，尝试查找包含学校名称的段落
            school_pattern = r'(?:大学|学院|学校)[^，。\n]{0,30}'
            school_matches = re.finditer(school_pattern, text)
            for match in school_matches:
                context = text[max(0, match.start()-50):min(len(text), match.end()+50)]
                if len(context) > 10:
                    education.append(context.strip())
            
            if education:
                logger.info(f"通过学校名称提取到{len(education)}条教育经历")
                return education
            
            logger.warning("未找到教育经历")
            return []
        except Exception as e:
            logger.error(f"教育经历提取失败: {str(e)}")
            return []
    
    def _extract_work_experience(self, text):
        """提取工作经历"""
        try:
            experience = []
            # 扩展工作经历匹配模式
            exp_patterns = [
                r'(?:工作经历|工作经验|工作背景|工作履历)[：:]\s*(.*?)(?=\n\n|\Z)',
                r'(?:工作经历|工作经验|工作背景|工作履历)\s*(.*?)(?=\n\n|\Z)',
            ]
            
            for pattern in exp_patterns:
                match = re.search(pattern, text, re.DOTALL)
                if match:
                    exp_text = match.group(1)
                    # 改进分割逻辑
                    exp_items = re.split(r'\n(?=\d{4}|\d{2}年)', exp_text)
                    for item in exp_items:
                        if item.strip():
                            # 清理和标准化工作经历
                            item = re.sub(r'\s+', ' ', item.strip())
                            if len(item) > 10:  # 过滤掉太短的条目
                                experience.append(item)
                    if experience:
                        logger.info(f"提取到{len(experience)}条工作经历")
                        return experience
            
            # 如果没有找到明确的工作经历标记，尝试查找包含公司名称的段落
            company_pattern = r'(?:公司|企业|集团)[^，。\n]{0,30}'
            company_matches = re.finditer(company_pattern, text)
            for match in company_matches:
                context = text[max(0, match.start()-100):min(len(text), match.end()+100)]
                if len(context) > 20:
                    experience.append(context.strip())
            
            if experience:
                logger.info(f"通过公司名称提取到{len(experience)}条工作经历")
                return experience
            
            logger.warning("未找到工作经历")
            return []
        except Exception as e:
            logger.error(f"工作经历提取失败: {str(e)}")
            return []
    
    def _extract_skills(self, text):
        """提取技能"""
        try:
            skills = []
            # 扩展技能匹配模式
            skill_patterns = [
                r'(?:技能特长|专业技能|技术技能|个人技能|核心技能)[：:]\s*(.*?)(?=\n\n|\Z)',
                r'(?:技能特长|专业技能|技术技能|个人技能|核心技能)\s*(.*?)(?=\n\n|\Z)',
            ]
            
            for pattern in skill_patterns:
                match = re.search(pattern, text, re.DOTALL)
                if match:
                    skill_text = match.group(1)
                    # 改进分割逻辑
                    skill_items = re.split(r'[,，、；;]', skill_text)
                    for item in skill_items:
                        if item.strip():
                            # 清理和标准化技能
                            item = re.sub(r'\s+', ' ', item.strip())
                            if len(item) > 2:  # 过滤掉太短的条目
                                skills.append(item)
                    if skills:
                        logger.info(f"提取到{len(skills)}个技能")
                        return skills
            
            # 如果没有找到明确的技能标记，尝试查找包含常见技能关键词的段落
            skill_keywords = ['精通', '熟悉', '掌握', '了解', '熟练', '擅长', '熟练使用', '熟练操作']
            for keyword in skill_keywords:
                keyword_matches = re.finditer(keyword + r'[^，。\n]{0,30}', text)
                for match in keyword_matches:
                    skill = match.group(0).strip()
                    if len(skill) > 3:
                        skills.append(skill)
            
            if skills:
                logger.info(f"通过关键词提取到{len(skills)}个技能")
                return skills
            
            logger.warning("未找到技能信息")
            return []
        except Exception as e:
            logger.error(f"技能提取失败: {str(e)}")
            return [] 