# Generated by Django 4.0.6 on 2022-11-12 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emsi', '0010_alter_employee_emp_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='emp_id',
            field=models.CharField(default='emp828', max_length=70),
        ),
    ]
