# Generated by Django 4.2.4 on 2024-02-06 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard_app', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='realcostinternspending',
            name='date',
        ),
        migrations.AddField(
            model_name='realcostinternspending',
            name='date_cost',
            field=models.DateField(auto_now=True),
        ),
    ]
