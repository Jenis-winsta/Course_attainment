# Generated by Django 4.2.7 on 2024-04-10 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charts', '0024_remove_file_description_year_of_file_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file_description',
            name='passout_year',
            field=models.CharField(max_length=4),
        ),
    ]
