# Generated by Django 4.2.4 on 2023-10-02 08:34

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard_app', '0004_contact_id_odoo_contact_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountAnalyticGroup',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(db_index=True, max_length=100)),
                ('id_odoo', models.SmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='AccountAnalyticAccount',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(db_index=True, max_length=100)),
                ('code', models.CharField(db_index=True, max_length=100)),
                ('id_odoo', models.SmallIntegerField()),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard_app.accountanalyticgroup')),
            ],
        ),
    ]