# Generated by Django 5.1.5 on 2025-05-15 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PaymentMethod', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentmethod',
            name='expiration_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
