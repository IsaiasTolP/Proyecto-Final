# Generated by Django 5.1.5 on 2025-05-18 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_alter_projectimage_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectcategory',
            name='icon',
            field=models.CharField(default='fa-solid fa-question', max_length=50),
        ),
    ]
