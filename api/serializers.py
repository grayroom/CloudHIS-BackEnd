from rest_framework import serializers
from api.models import Template, Appointment, Diagnosis, Symptom, Prescript, \
    Patient, Doctor, User, NerHistory


class TemplatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = '__all__'


class DiagnosisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnosis
        fields = '__all__'


class NewDiagnosisSerializer(serializers.ModelSerializer):

    class Meta:
        model = Diagnosis
        fields = ('id', 'appointment_id', 'patient_id', 'doctor_id', 'begin_at',
                  'diag_type', 'comment', 'named_entity')


class SymptomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symptom
        fields = '__all__'


class PrescriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescript
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'


class AppointmentSerializer(serializers.ModelSerializer):
    patient_id = PatientSerializer(read_only=True)
    doctor_id = DoctorSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = ('id', 'patient_id', 'doctor_id', 'begin_at', 'begin_at',
                  'category', 'status', 'created_time', 'updated_time',
                  'preliminary')


class NewAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ('patient_id', 'doctor_id', 'begin_at', 'begin_at',
                  'category', 'status', 'created_time', 'updated_time',
                  'preliminary')


class NerHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NerHistory
        fields = '__all__'


class PatientDiagnosisSerializer(serializers.ModelSerializer):
    appointment_id = AppointmentSerializer(read_only=True)
    doctor_id = DoctorSerializer(read_only=True)

    class Meta:
        model = Diagnosis
        fields = ('id', 'appointment_id', 'patient_id', 'doctor_id', 'begin_at',
                  'diag_type', 'comment', 'named_entity', 'created_time', 'updated_time')
