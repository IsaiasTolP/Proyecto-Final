# Generated by Django 5.1.5 on 2025-05-13 12:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contributions', '0002_contribution_message'),
        ('projects', '0005_alter_projectimage_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contribution',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='project_contributions', to='projects.project'),
        ),
    ]
