# Generated by Django 4.1.5 on 2023-01-11 19:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('is_superuser', models.BooleanField()),
                ('username', models.CharField(max_length=150, unique=True)),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('email', models.CharField(max_length=254)),
                ('is_staff', models.BooleanField()),
                ('is_active', models.BooleanField()),
                ('date_joined', models.DateTimeField()),
            ],
            options={
                'db_table': 'auth_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(help_text='appointment ID', primary_key=True, serialize=False)),
                ('begin_at', models.DateTimeField()),
                ('category', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=50)),
                ('preliminary', models.CharField(blank=True, max_length=5000, null=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Diagnosis',
            fields=[
                ('id', models.BigIntegerField(help_text='diagnosis ID', primary_key=True, serialize=False)),
                ('begin_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('diag_type', models.CharField(blank=True, max_length=50, null=True)),
                ('comment', models.CharField(blank=True, max_length=5000, null=True)),
                ('named_entity', models.JSONField(blank=True, default=dict, null=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('appointment_id', models.ForeignKey(blank=True, db_column='appointment_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='api.appointment')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_ptr', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='api.authuser')),
                ('name', models.CharField(max_length=50)),
                ('dob', models.DateField()),
                ('sex', models.CharField(max_length=10)),
                ('address', models.CharField(max_length=100)),
                ('join_date', models.DateTimeField()),
                ('phone_number', models.CharField(max_length=128)),
                ('authority', models.IntegerField()),
            ],
            options={
                'db_table': 'auths_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.BigAutoField(help_text='Post ID', primary_key=True, serialize=False)),
                ('is_directory', models.BooleanField(default=False)),
                ('file_name', models.CharField(max_length=50)),
                ('file_content', models.JSONField(default=dict)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('parent_id', models.ForeignKey(blank=True, db_column='parent_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='api.template')),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('user_idx', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='api.user')),
                ('subject', models.CharField(default=None, max_length=50, null=True)),
                ('position', models.CharField(max_length=50)),
                ('room', models.CharField(default=None, max_length=50, null=True)),
                ('dept_idx', models.IntegerField(default=None, null=True)),
                ('sup_idx', models.IntegerField(default=None, null=True)),
            ],
            options={
                'db_table': 'auths_doctor',
                'managed': False,
            },
            bases=('api.user',),
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('user_idx', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='api.user')),
                ('doc_idx', models.IntegerField(default=0)),
                ('is_admission', models.BooleanField(default=False)),
                ('room', models.CharField(default=None, max_length=50, null=True)),
            ],
            options={
                'db_table': 'auths_patient',
                'managed': False,
            },
            bases=('api.user',),
        ),
        migrations.CreateModel(
            name='Symptom',
            fields=[
                ('id', models.BigAutoField(help_text='symptom ID', primary_key=True, serialize=False)),
                ('s_code', models.CharField(max_length=50)),
                ('s_onset', models.DateTimeField()),
                ('s_severity', models.CharField(max_length=50)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('appointment_id', models.ForeignKey(blank=True, db_column='appointment_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='api.appointment')),
                ('doctor_id', models.ForeignKey(blank=True, db_column='doctor_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='symptom_publisher', to='api.user')),
                ('patient_id', models.ForeignKey(blank=True, db_column='patient_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='symptom_patient', to='api.user')),
            ],
        ),
        migrations.CreateModel(
            name='Prescript',
            fields=[
                ('id', models.BigAutoField(help_text='prescript ID', primary_key=True, serialize=False)),
                ('medicine_code', models.CharField(max_length=50)),
                ('quantity', models.IntegerField()),
                ('medicine_unit', models.CharField(max_length=50)),
                ('medicine_begin_time', models.DateTimeField()),
                ('medicine_end_time', models.DateTimeField()),
                ('medicine_dose_unit', models.CharField(max_length=50)),
                ('medicine_dose', models.IntegerField()),
                ('medicine_usage', models.CharField(max_length=50)),
                ('comment', models.CharField(max_length=500)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('appointment_id', models.ForeignKey(blank=True, db_column='appointment_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='api.appointment')),
                ('doctor_id', models.ForeignKey(blank=True, db_column='doctor_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prescript_publisher', to='api.user')),
                ('patient_id', models.ForeignKey(blank=True, db_column='patient_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prescript_patient', to='api.user')),
            ],
        ),
        migrations.CreateModel(
            name='NerHistory',
            fields=[
                ('id', models.BigIntegerField(help_text='ner history ID', primary_key=True, serialize=False)),
                ('target_text', models.TextField(blank=True, null=True)),
                ('ner_result', models.JSONField(blank=True, default=dict, null=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('diag_id', models.ForeignKey(blank=True, db_column='diag_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='api.diagnosis')),
                ('doctor_id', models.ForeignKey(blank=True, db_column='doctor_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ner_publisher', to='api.user')),
                ('patient_id', models.ForeignKey(blank=True, db_column='patient_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ner_patient', to='api.user')),
            ],
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='doctor_id',
            field=models.ForeignKey(blank=True, db_column='doctor_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='diagonsis_publisher', to='api.user'),
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='patient_id',
            field=models.ForeignKey(blank=True, db_column='patient_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='diagnosis_patient', to='api.user'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='doctor_id',
            field=models.ForeignKey(blank=True, db_column='doctor_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='doctor_ref_id', to='api.doctor'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='patient_id',
            field=models.ForeignKey(blank=True, db_column='patient_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='patient_ref_id', to='api.patient'),
        ),
    ]
