# Generated by Django 2.0 on 2020-01-24 07:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0007_auto_20200121_1924'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='read_num',
            name='blog',
        ),
        migrations.AlterModelOptions(
            name='blog',
            options={},
        ),
        migrations.DeleteModel(
            name='Read_Num',
        ),
    ]
