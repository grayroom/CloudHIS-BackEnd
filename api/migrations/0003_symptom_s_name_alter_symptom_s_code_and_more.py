# Generated by Django 4.1.5 on 2023-01-11 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_remove_prescript_appointment_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='symptom',
            name='s_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='symptom',
            name='s_code',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='symptom',
            name='s_onset',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='symptom',
            name='s_severity',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
