# Generated by Django 5.2 on 2025-05-13 11:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='holiday',
            options={'ordering': ['date'], 'verbose_name': 'Holiday', 'verbose_name_plural': 'Holidays'},
        ),
    ]
