# Generated by Django 4.2.4 on 2023-10-03 06:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard_app', '0008_MANUAL_CREATE_EXAMPLE_20231002_1656'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='prenom',
        ),
    ]
