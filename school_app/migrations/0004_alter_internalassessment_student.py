# Generated by Django 5.1.5 on 2025-04-04 14:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school_app', '0003_alter_internalassessment_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='internalassessment',
            name='student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='school_app.student'),
        ),
    ]
