# Generated by Django 3.1.7 on 2022-03-15 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0004_auto_20220315_1029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicemodel',
            name='name',
            field=models.CharField(max_length=30, unique=True, verbose_name='服务名称'),
        ),
    ]