# Generated by Django 5.1.5 on 2025-05-05 18:27

import imagekit.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_alter_project_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectimage',
            name='image',
            field=imagekit.models.fields.ProcessedImageField(default='default.jpg', upload_to='project_images/'),
        ),
    ]
