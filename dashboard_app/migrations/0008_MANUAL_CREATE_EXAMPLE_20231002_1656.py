# Generated by Django 4.2.4 on 2023-10-02 12:56
import random

from django.db import migrations

from dashboard_app.models import Contact
from faker import Faker

def add_example_contact(apps, schema_editor):
    fake = Faker()
    for i in range(10):
        Contact.objects.create(
            email=fake.email(),
            id_odoo=fake.random_digit(),
            type= random.choice(('M','B')),
            nom=fake.first_name(),
            prenom=fake.last_name(),
            structure=fake.company(),
            role=fake.job(),
            tel=fake.phone_number(),
            adresse=fake.address(),
        )

def reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('dashboard_app', '0007_alter_configuration_odoo_apikey_and_more'),
    ]

    operations = [
        migrations.RunPython(add_example_contact, reverse)
    ]
