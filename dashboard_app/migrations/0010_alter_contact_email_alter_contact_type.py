# Generated by Django 4.2.4 on 2023-10-03 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard_app', '0009_remove_contact_prenom'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='email',
            field=models.EmailField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='type',
            field=models.CharField(choices=[('M', 'membership'), ('B', 'beneficiarie')], default='B', max_length=1),
        ),
    ]
