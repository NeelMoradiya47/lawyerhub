# Generated by Django 5.0.1 on 2024-01-22 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lawyerhub', '0006_alter_client_contact_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lawyer',
            name='passing_year',
            field=models.CharField(max_length=100),
        ),
    ]