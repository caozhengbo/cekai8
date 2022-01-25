# Generated by Django 3.2.9 on 2022-01-24 06:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CaseModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200, verbose_name='用例名称')),
                ('relation', models.CharField(max_length=50, verbose_name='节点id')),
                ('length', models.IntegerField(verbose_name='API个数')),
                ('tag', models.IntegerField(choices=[(1, '冒烟用例'), (2, '集成用例'), (3, '监控脚本'), (4, '回归用例'), (5, '系统用例'), (6, '空库用例')], default=2, verbose_name='用例标签')),
            ],
            options={
                'db_table': 'case',
            },
        ),
        migrations.CreateModel(
            name='ProjectMode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('desc', models.CharField(max_length=100)),
                ('responsible', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'project',
            },
        ),
        migrations.CreateModel(
            name='VariableModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('key', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=1024)),
                ('desc', models.CharField(max_length=500, null=True, verbose_name='简要介绍')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='test_runner.projectmode')),
            ],
            options={
                'db_table': 'variable',
            },
        ),
        migrations.CreateModel(
            name='ReportModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100, verbose_name='报告名称')),
                ('type', models.IntegerField(choices=[(1, '调试'), (2, '异步'), (3, '定时')], verbose_name='报告类型')),
                ('summary', models.TextField(verbose_name='简要主体信息')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='test_runner.projectmode')),
            ],
            options={
                'verbose_name': '测试报告',
                'verbose_name_plural': '测试报告',
            },
        ),
        migrations.CreateModel(
            name='ReportDetailModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100, verbose_name='报告名称')),
                ('summary', models.TextField(verbose_name='主体信息')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='test_runner.projectmode')),
                ('report', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='test_runner.reportmodel')),
            ],
            options={
                'verbose_name': '测试报告详情',
                'verbose_name_plural': '测试报告详情',
            },
        ),
        migrations.CreateModel(
            name='RelationModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tree', models.TextField(default=[], verbose_name='结构主题')),
                ('type', models.IntegerField(default=1, verbose_name='树类型')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='test_runner.projectmode')),
            ],
            options={
                'verbose_name': '树形结构关系',
                'db_table': 'relation',
            },
        ),
        migrations.CreateModel(
            name='HostIPModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100, verbose_name='HOST配置名称')),
                ('value', models.TextField(verbose_name='配置值')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='test_runner.projectmode')),
            ],
            options={
                'db_table': 'hostip',
            },
        ),
        migrations.CreateModel(
            name='DebugtalkModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.TextField(default='# write you code', verbose_name='python代码')),
                ('project', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='test_runner.projectmode')),
            ],
            options={
                'verbose_name': '驱动文件表',
                'verbose_name_plural': '驱动文件表',
                'db_table': 'Debugtalk',
            },
        ),
        migrations.CreateModel(
            name='ConfigModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100, verbose_name='环境名称')),
                ('body', models.TextField(verbose_name='主体信息')),
                ('base_url', models.CharField(max_length=100, verbose_name='请求地址')),
                ('configdesc', models.CharField(blank=True, max_length=500, null=True, verbose_name='简要介绍')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='test_runner.projectmode')),
            ],
            options={
                'db_table': 'config',
            },
        ),
        migrations.CreateModel(
            name='CaseStepModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200, verbose_name='用例名称')),
                ('body', models.TextField(verbose_name='主体信息')),
                ('url', models.CharField(max_length=500, verbose_name='请求地址')),
                ('method', models.CharField(max_length=10, verbose_name='请求方式')),
                ('step', models.IntegerField(verbose_name='顺序')),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='test_runner.casemodel')),
            ],
            options={
                'verbose_name': '用例信息step表',
                'db_table': 'casestep',
            },
        ),
        migrations.AddField(
            model_name='casemodel',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='test_runner.projectmode'),
        ),
        migrations.CreateModel(
            name='ApiModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=500, verbose_name='接口名称')),
                ('body', models.TextField(verbose_name='主体信息')),
                ('url', models.CharField(max_length=500, verbose_name='请求地址')),
                ('method', models.CharField(max_length=10, verbose_name='请求方式')),
                ('relation', models.CharField(max_length=50, verbose_name='节点id')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='test_runner.projectmode')),
            ],
            options={
                'verbose_name': 'API信息表',
                'db_table': 'api',
            },
        ),
        migrations.CreateModel(
            name='PycodeModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('code', models.TextField(default='# _*_ coding:utf-8 _*_', verbose_name='python代码')),
                ('name', models.CharField(max_length=30)),
                ('desc', models.CharField(blank=True, max_length=100, null=True, verbose_name='简要介绍')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='test_runner.projectmode')),
            ],
            options={
                'verbose_name': '驱动文件库',
                'verbose_name_plural': '驱动文件库',
                'unique_together': {('project', 'name')},
            },
        ),
        migrations.CreateModel(
            name='ModelWithFileFieldModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
                ('file', models.FileField(blank=True, null=True, unique=True, upload_to='testdatas')),
                ('relation', models.CharField(max_length=50, verbose_name='节点id')),
                ('excel_tree', models.TextField(blank=True, null=True, verbose_name='excel的级联数据')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='test_runner.projectmode')),
            ],
            options={
                'verbose_name': '文件信息表',
                'verbose_name_plural': '文件信息表',
                'unique_together': {('project', 'name')},
            },
        ),
    ]
