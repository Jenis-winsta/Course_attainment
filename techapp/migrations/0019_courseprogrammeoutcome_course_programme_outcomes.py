# Generated by Django 4.2.7 on 2024-03-30 13:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('techapp', '0018_course_assigned_to'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseProgrammeOutcome',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('strength', models.PositiveSmallIntegerField(default=1)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='techapp.course')),
                ('programme_outcome', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='techapp.programme_outcome')),
            ],
            options={
                'unique_together': {('course', 'programme_outcome')},
            },
        ),
        migrations.AddField(
            model_name='course',
            name='programme_outcomes',
            field=models.ManyToManyField(through='techapp.CourseProgrammeOutcome', to='techapp.programme_outcome'),
        ),
    ]
