# Generated by Django 5.0.1 on 2024-01-23 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lawyerhub', '0007_alter_lawyer_passing_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='first_name',
            field=models.CharField(default=None, max_length=255),
        ),
        migrations.AddField(
            model_name='booking',
            name='last_name',
            field=models.CharField(default=None, max_length=255),
        ),
    ]
