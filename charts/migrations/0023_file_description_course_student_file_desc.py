# Generated by Django 5.0.1 on 2024-04-08 12:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charts', '0022_remove_file_description_course_and_more'),
        ('techapp', '0020_rename_courseprogrammeoutcome_course_programme_outcome'),
    ]

    operations = [
        migrations.AddField(
            model_name='file_description',
            name='course',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='techapp.course'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='file_desc',
            field=models.ForeignKey(default=9, on_delete=django.db.models.deletion.CASCADE, to='charts.file_description'),
            preserve_default=False,
        ),
    ]
