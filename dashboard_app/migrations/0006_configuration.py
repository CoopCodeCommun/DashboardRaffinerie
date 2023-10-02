# Generated by Django 4.2.4 on 2023-10-02 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard_app', '0005_accountanalyticgroup_accountanalyticaccount'),
    ]

    operations = [
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qonto_login', models.CharField(max_length=100)),
                ('qonto_apikey', models.CharField(max_length=100)),
                ('odoo_url', models.URLField()),
                ('odoo_login', models.CharField(max_length=100)),
                ('odoo_apikey', models.CharField(max_length=100)),
                ('odoo_dbname', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
