from django.urls import path, re_path
from api import views, kafkaAdapters
from django.views.generic.base import RedirectView

urlpatterns = [
    #     path('emr/api/templates/', views.templates_list, name='templates_list'),
    #     path('emr/api/templates/<int:id>/', views.templates_detail, name='templates_detail'),

    path('emr/api/prescription/list/', views.PrescriptionsView.as_view(),
         name='prescriptions_list'),
    path('emr/api/prescript/', views.PrescriptionView.as_view(),
         name='prescription'),

    path('emr/api/emr/list/', views.PatientDiagnosisView.as_view(),
         name='diagnosis_list'),

    # NOTE: 이미 생성된 appointment를 가져오는 API
    path('emr/api/appointment/list/', views.AppointmentsView.as_view(),
         name='appointments_list'),
    # NOTE: 단일 appointment에 대한 API
    path('emr/api/appointment/', views.AppointmentView.as_view(),
         name='appointment'),

    path('emr/api/symptom/list/', views.PatientSymptomView.as_view(),
         name='patient_symptom_list'),
    path('emr/api/prescript/list/', views.PatientPrescriptView.as_view(),
         name='patient_prescript_list'),

    path('emr/api/issueEMR/', kafkaAdapters.IssueMessage.as_view(),
         name='issueEMR'),

    # Vue.js routing
    re_path(r'^emr/', views.HomeView.as_view(), name='home'),
    path('', RedirectView.as_view(url='/emr/')),
]
