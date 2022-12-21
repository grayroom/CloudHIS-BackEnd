# Generated by Django 4.1 on 2022-11-25 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_prescript_named_entity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prescript',
            name='named_entity',
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='named_entity',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AlterField(
            model_name='diagnosis',
            name='begin_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='diagnosis',
            name='comment',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='diagnosis',
            name='diag_type',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='diagnosis',
            name='end_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]