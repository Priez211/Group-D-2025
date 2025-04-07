# Generated by Django 5.1.5 on 2025-03-17 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aits', '0003_alter_issue_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='priority',
            field=models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='medium', max_length=10),
        ),
        migrations.AddField(
            model_name='issue',
            name='title',
            field=models.CharField(default='Untitled Issue', max_length=200),
        ),
    ]
