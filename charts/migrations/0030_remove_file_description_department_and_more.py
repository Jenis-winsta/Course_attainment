# Generated by Django 4.2.7 on 2024-04-10 09:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('charts', '0029_passoutyear_alter_file_description_passout_year'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file_description',
            name='department',
        ),
        migrations.RemoveField(
            model_name='file_description',
            name='semester',
        ),
        migrations.RemoveField(
            model_name='file_description',
            name='year',
        ),
    ]
