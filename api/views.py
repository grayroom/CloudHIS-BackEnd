from django.shortcuts import get_list_or_404, get_object_or_404
from django.views.generic import TemplateView
from django.utils.datetime_safe import datetime
from django.utils.dateparse import parse_datetime
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Diagnosis, Prescript, Appointment, \
    Patient, Symptom
from api.permissions import IsAuthorizedUser
from api.serializers import TemplatesSerializer, SymptomSerializer, \
    DiagnosisSerializer, PrescriptSerializer, AppointmentSerializer, \
    PatientSerializer, DoctorSerializer, NewAppointmentSerializer, \
    NewDiagnosisSerializer, PatientDiagnosisSerializer


from config import settings
import jwt
import json


class HomeView(TemplateView):
    template_name = 'index.html'


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


class AppointmentsView(APIView):
    permission_classes([IsAuthorizedUser])
    appointment_serializer_class = AppointmentSerializer

    def post(self, request):
        target_date = parse_datetime(request.data['begin_at'])
        appointment_list = Appointment.objects.filter(
            doctor_id=request.data['doctor_idx'],
            begin_at__year=target_date.year,
            begin_at__month=target_date.month,
            begin_at__day=target_date.day).select_related('patient_id', 'doctor_id')

        serializer = self.appointment_serializer_class(
            instance=appointment_list, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class AppointmentView(APIView):
    permission_classes([IsAuthorizedUser])
    appointment_serializer_class = AppointmentSerializer
    new_appointment_serializer_class = NewAppointmentSerializer

    def get(self, request):
        appointment = Appointment.objects.filter(
            id=request.GET['idx']).select_related('patient_id', 'doctor_id')
        serializer = self.appointment_serializer_class(appointment, many=True)

        return Response(serializer.data[0], status=status.HTTP_200_OK)

    def post(self, request):
        appo_serializer = self.new_appointment_serializer_class(
            data=request.data)

        if appo_serializer.is_valid():
            appo_serializer.save()

            return Response(appo_serializer.data, status=status.HTTP_201_CREATED)
        return Response(appo_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PrescriptionView(APIView):
    permission_classes([IsAuthorizedUser])
    diagnosis_serializer_class = DiagnosisSerializer
    symptom_serializer_class = SymptomSerializer
    prescript_serializer_class = PrescriptSerializer

    # make new multiple prescriptions(medicine: tr), multiple symptoms, diagnosis
    def post(self, request):
        payload = get_payload(request)

        # make new multiple prescriptions(medicine: tr), multiple symptoms, diagnosis for reserved patient
        if request.data['is_reserved']:
            # update appointment data identified by appointment_id
            appointment = Appointment.objects.get(
                id=request.data['appointment_id'])
            appointment.status = 'done'
            appointment.preliminary = request.data['preliminary']
            appointment.save()

            request.data.pop('is_reserved')
            request.data.pop('patient_info')
            request.data.pop('preliminary')
            request.data['doctor_id'] = payload['user_id']
            request.data['end_at'] = datetime.now()

            # add diagnosis information
            diag_serializer = self.diagnosis_serializer_class(
                data=request.data)
            if diag_serializer.is_valid(raise_exception=True):
                diag_serializer.save()

            # add symptom information for each unique named_entity pr data
            for pr in request.data['named_entity']['pr']:
                new_symptom = {
                    'patient_id': request.data['patient_id'],
                    'doctor_id': payload['user_id'],
                    'diagnosis_id': diag_serializer.data['id'],
                    's_name': pr['keyword'],
                    's_severity': pr['severity'],
                    's_onset': pr['onset'],
                }
                symptom_serializer = self.symptom_serializer_class(
                    data=new_symptom)
                symptom_serializer.is_valid(raise_exception=True)
                symptom_serializer.save()

            # add prescription information for each unique named_entity tr data
            for tr in request.data['named_entity']['tr']:
                new_prescript = {
                    'patient_id': request.data['patient_id'],
                    'doctor_id': payload['user_id'],
                    'diagnosis_id': diag_serializer.data['id'],
                    'medicine_name': tr['keyword'],
                    'quantity': tr['quantity'],
                    'medicine_begin_time': tr['begin_time']
                }
                prescript_serializer = self.prescript_serializer_class(
                    data=new_prescript)
                prescript_serializer.is_valid(raise_exception=True)
                prescript_serializer.save()

            return Response(diag_serializer.data, status=status.HTTP_200_OK)
        else:
            # return with 400
            return Response(status=status.HTTP_400_BAD_REQUEST)


class PatientInChargeView(APIView):
    permission_classes([IsAuthorizedUser])
    patient_in_charge_serializer_class = PatientSerializer

    def post(self, request):
        patient_list = get_list_or_404(Patient,
                                       doc_idx=request.data['doctor_idx'])
        serializer = PatientSerializer(patient_list, many=True)
        serializer.is_valid()

        return Response(serializer.data, status=status.HTTP_200_OK)


class PatientSymptomView(APIView):
    permission_classes([IsAuthorizedUser])
    symptom_serializer_class = SymptomSerializer
    symptom_model = Symptom.objects

    def post(self, request):
        symptom_list = self.symptom_model.filter(
            patient_id=request.data['patient_idx']
        )
        serializer = SymptomSerializer(data=symptom_list, many=True)
        serializer.is_valid()

        return Response(serializer.data, status=status.HTTP_200_OK)


class PatientPrescriptView(APIView):
    permission_classes([IsAuthorizedUser])
    prescript_serializer_class = PrescriptSerializer
    prescript_model = Prescript.objects

    def post(self, request):
        prescript_list = self.prescript_model.filter(
            patient_id=request.data['patient_idx']
        )
        serializer = PrescriptSerializer(data=prescript_list, many=True)
        serializer.is_valid()

        return Response(serializer.data, status=status.HTTP_200_OK)


class PatientDiagnosisView(APIView):
    permission_classes([IsAuthorizedUser])
    patient_diagnosis_serializer_class = PatientDiagnosisSerializer

    # get all diagnosis by patient_id
    def post(self, request):
        diagnosis_list = Diagnosis.objects.filter(
            patient_id=request.data['patient_idx']).select_related('appointment_id', 'patient_id')
        serializer = self.patient_diagnosis_serializer_class(
            instance=diagnosis_list, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


def get_payload(req):
    token = req.headers.get("Authorization", None)
    access_token = token.split(" ")[1]
    return jwt.decode(access_token,
                      settings.SIMPLE_JWT['VERIFYING_KEY'],
                      algorithms=[settings.SIMPLE_JWT['ALGORITHM']])
