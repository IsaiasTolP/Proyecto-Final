# Generated by Django 5.1.5 on 2025-05-08 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contributions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contribution',
            name='message',
            field=models.CharField(blank=True, max_length=140),
        ),
    ]
