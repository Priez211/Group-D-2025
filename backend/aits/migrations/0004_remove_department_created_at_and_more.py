# Generated by Django 5.1.7 on 2025-03-11 11:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aits', '0003_department_issue_category_alter_issue_assigned_to_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='department',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='department',
            name='updated_at',
        ),
    ]
