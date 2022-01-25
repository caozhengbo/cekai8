from django.db import models
import sys

# sys.executable
# HttpRunner

"""
python manage.py makemigrations
python manage.py migrate
"""


# Create your models here.

class BaseModel(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # 表示夫模型不在数据中生成表，而是将属性写入到子模型的表中


class ProjectMode(BaseModel):
    # 项目主键 id
    # 项目名称
    # 项目描述
    # 项目创建人
    name = models.CharField(max_length=100, unique=True, null=False)  # max_length长度  unique是否唯一 null不能为空
    desc = models.CharField(max_length=100, null=False)
    responsible = models.CharField(max_length=20, null=False)

    class Meta:
        db_table = "project"


class VariableModel(BaseModel):
    class Meta:
        db_table = "variable"

    key = models.CharField(null=False, max_length=100)
    value = models.CharField(null=False, max_length=1024)
    desc = models.CharField("简要介绍", max_length=500, null=True)
    project = models.ForeignKey(ProjectMode, on_delete=models.CASCADE)  # 设置外键


class ConfigModel(BaseModel):
    class Meta:
        db_table = "config"

    name = models.CharField("环境名称", null=False, max_length=100)
    body = models.TextField("主体信息", null=False)
    base_url = models.CharField("请求地址", null=False, max_length=100)
    configdesc = models.CharField("简要介绍", max_length=500, null=True, blank=True)
    project = models.ForeignKey(to=ProjectMode, on_delete=models.CASCADE)


class HostIPModel(BaseModel):
    name = models.CharField("HOST配置名称", null=False, max_length=100)
    value = models.TextField("配置值", null=False)
    project = models.ForeignKey(ProjectMode, on_delete=models.CASCADE)

    class Meta:
        db_table = "hostip"


class RelationModel(models.Model):
    '''
    树形结构关系
    '''

    class Meta:
        verbose_name = "树形结构关系"
        db_table = "relation"

    project = models.ForeignKey(ProjectMode, on_delete=models.CASCADE)
    tree = models.TextField("结构主题", null=False, default=[])
    type = models.IntegerField("树类型", default=1)


class ApiModel(BaseModel):
    '''
    API信息表
    '''

    class Meta:
        verbose_name = "API信息表"
        db_table = "api"

    name = models.CharField("接口名称", null=False, max_length=500)
    body = models.TextField("主体信息", null=False)
    url = models.CharField("请求地址", null=False, max_length=500)
    method = models.CharField("请求方式", null=False, max_length=10)
    project = models.ForeignKey(ProjectMode, on_delete=models.CASCADE)
    relation = models.CharField("节点id", null=False, max_length=50)


class CaseModel(BaseModel):
    '''
    用例信息表
    '''

    class Meta:
        db_table = "case"

    tag = (
        (1, "冒烟用例"),
        (2, "集成用例"),
        (3, "监控脚本"),
        (4, "回归用例"),
        (5, "系统用例"),
        (6, "空库用例")
    )
    name = models.CharField("用例名称", null=False, max_length=200)
    project = models.ForeignKey(ProjectMode, on_delete=models.CASCADE)
    relation = models.CharField("节点id", null=False, max_length=50)
    length = models.IntegerField("API个数", null=False)
    tag = models.IntegerField("用例标签", choices=tag, default=2)


class CaseStepModel(BaseModel):
    '''
    用例信息step表
    '''

    class Meta:
        verbose_name = "用例信息step表"
        db_table = "casestep"

    name = models.CharField("用例名称", null=False, max_length=200)
    body = models.TextField("主体信息", null=False)
    url = models.CharField("请求地址", null=False, max_length=500)
    method = models.CharField("请求方式", null=False, max_length=10)
    case = models.ForeignKey(CaseModel, on_delete=models.CASCADE)
    step = models.IntegerField("顺序", null=False)


class PycodeModel(BaseModel):
    """
    驱动文件表
    """

    class Meta:
        verbose_name = "驱动文件库"
        verbose_name_plural = verbose_name
        unique_together = [['project', 'name']]
        # db_table = "pycode"

    code = models.TextField("python代码", default="# _*_ coding:utf-8 _*_", null=False)
    project = models.ForeignKey(ProjectMode, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, null=False)
    desc = models.CharField("简要介绍", max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class ReportModel(BaseModel):
    """
    报告存储
    """
    report_type = (
        (1, "调试"),
        (2, "异步"),
        (3, "定时")
    )

    class Meta:
        verbose_name = "测试报告"
        verbose_name_plural = verbose_name

    name = models.CharField("报告名称", null=False, max_length=100)
    type = models.IntegerField("报告类型", choices=report_type)
    summary = models.TextField("简要主体信息", null=False)
    project = models.ForeignKey(ProjectMode, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ReportDetailModel(BaseModel):
    """
    报告主题信息存储
    """

    class Meta:
        verbose_name = "测试报告详情"
        verbose_name_plural = verbose_name

    name = models.CharField("报告名称", null=False, max_length=100)
    summary = models.TextField("主体信息", null=False)
    project = models.ForeignKey(ProjectMode, on_delete=models.CASCADE)
    report = models.OneToOneField(ReportModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class DebugtalkModel(models.Model):
    """
    驱动文件表
    """

    class Meta:
        verbose_name = "驱动文件表"
        verbose_name_plural = verbose_name
        db_table = 'Debugtalk'

    code = models.TextField("python代码", default="# write you code", null=False)
    project = models.OneToOneField(to=ProjectMode, on_delete=models.CASCADE)


class ModelWithFileFieldModel(BaseModel):
    """
    文件信息表
    """

    class Meta:
        verbose_name = "文件信息表"
        verbose_name_plural = verbose_name
        unique_together = [['project', 'name']]

    project = models.ForeignKey(ProjectMode, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    file = models.FileField(upload_to='testdatas', unique=True, null=True, blank=True)
    relation = models.CharField("节点id", null=False, max_length=50)
    excel_tree = models.TextField("excel的级联数据", null=True, blank=True)

    def __str__(self):
        return self.name
