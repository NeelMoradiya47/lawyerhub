# Generated by Django 5.0.1 on 2024-03-22 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lawyerhub', '0014_booking_lawyer_contact_number_booking_lawyer_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='administrator',
            name='contact_number',
            field=models.CharField(default=None, max_length=15),
        ),
    ]
