# Generated by Django 3.1.7 on 2022-03-14 09:36

import backend.utils.model
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0002_testrolemodel'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceModel',
            fields=[
                ('id', models.SmallIntegerField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', backend.utils.model.CustomDateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', backend.utils.model.CustomDateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(db_index=True, max_length=30, verbose_name='服务名称')),
                ('domain', models.CharField(max_length=100, verbose_name='域名')),
                ('port', models.SmallIntegerField(verbose_name='端口号')),
                ('protocol', models.SmallIntegerField(choices=[(0, 'http'), (1, 'https'), (2, 'websocket'), (3, 'rpc'), (4, 'grpc')], default=0, verbose_name='协议')),
                ('flag', models.BooleanField(default=True, verbose_name='可用')),
            ],
            options={
                'verbose_name': '系统服务',
                'verbose_name_plural': '系统服务',
                'db_table': 'service',
            },
        ),
        migrations.CreateModel(
            name='ModuleModel',
            fields=[
                ('id', models.SmallIntegerField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', backend.utils.model.CustomDateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', backend.utils.model.CustomDateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(db_index=True, max_length=30, verbose_name='模块名称')),
                ('cls_name', models.CharField(db_index=True, max_length=50, verbose_name='自动化类名')),
                ('flag', models.BooleanField(default=True, verbose_name='可用')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='module', to=settings.AUTH_USER_MODEL, verbose_name='创建人')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='module', to='service.servicemodel', verbose_name='服务')),
            ],
            options={
                'verbose_name': '系统模块',
                'verbose_name_plural': '系统模块',
                'db_table': 'module',
            },
        ),
        migrations.CreateModel(
            name='InterfaceModel',
            fields=[
                ('id', models.SmallIntegerField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', backend.utils.model.CustomDateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', backend.utils.model.CustomDateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(db_index=True, max_length=30, unique=True, verbose_name='接口名称')),
                ('uri', models.CharField(max_length=50, verbose_name='接口URI')),
                ('flag', models.BooleanField(default=True, verbose_name='可用')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='interface', to=settings.AUTH_USER_MODEL, verbose_name='创建人')),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='interface', to='service.modulemodel', verbose_name='模块')),
            ],
            options={
                'verbose_name': '模块接口',
                'verbose_name_plural': '模块接口',
                'db_table': 'interface',
            },
        ),
        migrations.CreateModel(
            name='InterfaceDataModel',
            fields=[
                ('id', models.SmallIntegerField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', backend.utils.model.CustomDateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', backend.utils.model.CustomDateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(db_index=True, max_length=50, unique=True, verbose_name='数据包名')),
                ('interface', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='interface_data', to='service.interfacemodel', verbose_name='接口')),
                ('pre_interface_data', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='pre', to='service.interfacedatamodel', verbose_name='前置数据包')),
                ('test_role', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='interface_data', to='users.testrolemodel', verbose_name='测试角色')),
            ],
            options={
                'verbose_name': '接口数据包',
                'verbose_name_plural': '接口数据包',
                'db_table': 'interface_data',
            },
        ),
        migrations.CreateModel(
            name='InterfaceDataDetailModel',
            fields=[
                ('id', models.SmallIntegerField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', backend.utils.model.CustomDateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', backend.utils.model.CustomDateTimeField(auto_now=True, verbose_name='更新时间')),
                ('request', models.JSONField(verbose_name='请求数据')),
                ('response', models.JSONField(verbose_name='期望响应数据')),
                ('interface_data', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='detail', to='service.interfacedatamodel', verbose_name='数据包')),
            ],
            options={
                'verbose_name': '接口数据包详情',
                'verbose_name_plural': '接口数据包详情',
                'db_table': 'interface_data_detail',
            },
        ),
    ]