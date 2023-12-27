# Generated by Django 5.0 on 2023-12-25 07:24

import django.core.validators
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hst_payroll_manager', '0005_alter_paymentcurrency_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tax',
            fields=[
                ('initial_range', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('final_range', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('tax_rate', models.DecimalField(decimal_places=0, default=0.0, max_digits=3, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('deduction', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
            ],
        ),
    ]
