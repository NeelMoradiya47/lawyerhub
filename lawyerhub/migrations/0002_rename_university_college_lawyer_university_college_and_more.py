# Generated by Django 5.0.1 on 2024-01-15 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lawyerhub', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lawyer',
            old_name='university_College',
            new_name='university_college',
        ),
        migrations.AlterField(
            model_name='client',
            name='image',
            field=models.ImageField(upload_to=''),
        ),
        migrations.AlterField(
            model_name='lawyer',
            name='image',
            field=models.ImageField(upload_to=''),
        ),
    ]
