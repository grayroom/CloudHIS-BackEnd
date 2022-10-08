from rest_framework import serializers
from api.models import Template, Appointment, Diagnosis, Symptom, Prescript


class TemplatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = '__all__'


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'


class DiagnosisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnosis
        fields = '__all__'


class SymptomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symptom
        fields = '__all__'


class PrescriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescript
        fields = '__all__'
