# Generated by Django 4.2.4 on 2023-09-30 09:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import stdimage.models
import stdimage.validators
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=100)),
                ('nom', models.CharField(blank=True, max_length=100, null=True)),
                ('prenom', models.CharField(blank=True, max_length=100, null=True)),
                ('structure', models.CharField(blank=True, max_length=100, null=True)),
                ('tel', models.CharField(blank=True, max_length=100, null=True)),
                ('adresse', models.CharField(blank=True, max_length=100, null=True)),
                ('image', stdimage.models.JPEGField(blank=True, force_min_size=False, null=True, upload_to='images/', validators=[stdimage.validators.MinSizeValidator(960, 540)], variations={'med': (960, 540), 'thumb': (270, 270, True)}, verbose_name='Image du contact')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
