from django.shortcuts import get_list_or_404
from django.views.generic import TemplateView
from django.utils.datetime_safe import datetime
from django.utils.dateparse import parse_datetime
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Template, Symptom, Diagnosis, Prescript, Appointment, \
    Patient
from api.permissions import IsAuthorizedUser
from api.serializers import TemplatesSerializer, SymptomSerializer, \
    DiagnosisSerializer, PrescriptSerializer, AppointmentSerializer, \
    PatientSerializer, DoctorSerializer


class HomeView(TemplateView):
    template_name = 'index.html'


@api_view(['GET', 'PUT', 'POST'])
def templates_list(request):
    permission_classes([IsAuthorizedUser])

    if request.method == 'GET':
        templates = Template.objects.all()
        serializer = TemplatesSerializer(templates, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        request.data['is_directory'] = False
        request.data['file_name'] = request.data.get('title')
        request.data['file_content'] = request.data.get('content')
        serializer = TemplatesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        serializer = TemplatesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def templates_detail(request, id):
    permission_classes([IsAuthorizedUser])

    try:
        templates = Template.objects.get(id=id)
    except Template.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TemplatesSerializer(templates)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TemplatesSerializer(templates, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        templates.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SymptomsView(APIView):
    symptom_serializer_class = SymptomSerializer
    # FIXME: authorize를 실제 환자에게 권한이 있는 사람한테만 해야함
    permission_classes([IsAuthorizedUser])

    def post(self, request):
        symptom_list = get_list_or_404(Symptom,
                                       patient_idx=request.data['patient_idx'])
        serializer = self.symptom_serializer_class(
            symptom_list.filter(patient_idx=request.data['patient_idx']),
            many=True)
        serializer.is_valid()

        return Response(serializer.data, status=status.HTTP_200_OK)


class PrescriptionsView(APIView):
    prescript_serializer_class = PrescriptSerializer
    permission_classes([IsAuthorizedUser])

    def post(self, request):
        prescript_list = get_list_or_404(Prescript,
                                         patient_idx=request.data[
                                             'patient_idx'])
        serializer = self.prescript_serializer_class(
            prescript_list.filter(patient_idx=request.data['patient_idx']),
            many=True)
        serializer.is_valid()

        return Response(serializer.data, status=status.HTTP_200_OK)


class DiagnosisView(APIView):
    diagnosis_serializer_class = DiagnosisSerializer
    permission_classes([IsAuthorizedUser])

    def post(self, request):
        diagnosis_list = get_list_or_404(Diagnosis,
                                         patient_idx=request.data[
                                             'patient_idx'])
        serializer = self.diagnosis_serializer_class(
            diagnosis_list.filter(patient_idx=request.data['patient_idx']),
            many=True)
        serializer.is_valid()

        return Response(serializer.data, status=status.HTTP_200_OK)


class AppointmentsView(APIView):
    appointment_serializer_class = AppointmentSerializer
    permission_classes([IsAuthorizedUser])

    def post(self, request):
        appointment_list = get_list_or_404(Appointment,
                                           doctor_id=request.data[
                                               'doctor_idx'])

        target_date = parse_datetime(request.data['begin_at'])

        serializer = self.appointment_serializer_class(
            appointment_list.filter(patient_idx=request.data['patient_idx'],
                                    begin_at__year=target_date.year,
                                    begin_at__month=target_date.month,
                                    begin_at__day=target_date.day),
            many=True)
        serializer.is_valid()

        return Response(serializer.data, status=status.HTTP_200_OK)


class PatientInChargeView(APIView):
    permission_classes([IsAuthorizedUser])
    patient_in_charge_serializer_class = PatientSerializer

    def post(self, request):
        patient_list = get_list_or_404(Patient,
                                       doctor_id=request.data[
                                           'doctor_idx'])
        serializer = PatientSerializer(
            patient_list.filter(doctor_id=request.data['doctor_idx']),
            many=True)
        serializer.is_valid()

        return Response(serializer.data, status=status.HTTP_200_OK)


class AppointmentView(APIView):
    permission_classes([IsAuthorizedUser])
    appointment_serializer_class = AppointmentSerializer

    def post(self, request):
        appo_serializer = self.appointment_serializer_class(data=request.data)

        if appo_serializer.is_valid():
            appo_serializer.save()
            return Response(appo_serializer.data,
                            status=status.HTTP_201_CREATED)
