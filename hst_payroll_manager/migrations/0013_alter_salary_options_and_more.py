# Generated by Django 5.0 on 2023-12-26 07:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hst_payroll_manager', '0012_rename_monthly_salary_salary_gross_salary_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='salary',
            options={'verbose_name_plural': 'Salaries'},
        ),
        migrations.AlterField(
            model_name='salary',
            name='red_cross_contribution',
            field=models.DecimalField(decimal_places=1, default=0.5, max_digits=3, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
    ]
