# Generated by Django 4.2.7 on 2024-03-02 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[('admin', 'Admin'), ('teacher', 'Teacher'), ('hod', 'HOD')], default='teacher', max_length=20),
        ),
    ]
