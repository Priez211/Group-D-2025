# Generated by Django 5.1.5 on 2025-03-20 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aits', '0010_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('student', 'Student'), ('lecturer', 'Lecturer'), ('registrar', 'Academic Registrar')], max_length=10),
        ),
    ]
