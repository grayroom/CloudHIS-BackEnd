from django.urls import path, re_path
from api import views


urlpatterns = [
    path('emr/api/templates/', views.templates_list, name='templates_list'),
    path('emr/api/templates/<int:id>/', views.templates_detail, name='templates_detail'),

    re_path(r'^emr/', views.HomeView.as_view(), name='home'),
]