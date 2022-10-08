from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User as _User

from phonenumber_field.modelfields import PhoneNumberField


class Template(models.Model):
    id = models.BigAutoField(help_text="Post ID", primary_key=True)
    parent_id = models.ForeignKey(
        "Template", on_delete=models.CASCADE, null=True, blank=True,
        db_column="parent_id")

    is_directory = models.BooleanField(default=False)
    file_name = models.CharField(max_length=50)
    file_content = models.JSONField(default=dict)

    created_time = models.DateTimeField(auto_now_add=True)


class Appointment(models.Model):
    id = models.BigAutoField(help_text="appointment ID", primary_key=True)
    patient_id = models.ForeignKey(
        "User", on_delete=models.CASCADE, null=True, blank=True,
        db_column="patient_id", related_name="patient")
    doctor_id = models.ForeignKey(
        "User", on_delete=models.CASCADE, null=True, blank=True,
        db_column="doctor_id", related_name="doctor")
    begin_at = models.DateTimeField()
    category = models.CharField(max_length=50)  # 진료, 검사, 수술, 상담
    status = models.CharField(max_length=50)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)


class Diagnosis(models.Model):
    id = models.BigAutoField(help_text="diagnosis ID", primary_key=True)
    appointment_id = models.ForeignKey(
        "Appointment", on_delete=models.CASCADE, null=True, blank=True,
        db_column="appointment_id")
    patient_id = models.ForeignKey(
        "User", on_delete=models.CASCADE, null=True, blank=True,
        db_column="patient_id", related_name="diagnosis_patient")
    doctor_id = models.ForeignKey(
        "User", on_delete=models.CASCADE, null=True, blank=True,
        db_column="doctor_id", related_name="diagonsis_publisher")
    begin_time = models.DateTimeField()
    end_time = models.DateTimeField()
    diag_type = models.CharField(max_length=50)
    comment = models.CharField(max_length=500)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)


class Symptom(models.Model):
    id = models.BigAutoField(help_text="symptom ID", primary_key=True)
    appointment_id = models.ForeignKey(
        "Appointment", on_delete=models.CASCADE, null=True, blank=True,
        db_column="appointment_id")
    patient_id = models.ForeignKey(
        "User", on_delete=models.CASCADE, null=True, blank=True,
        db_column="patient_id", related_name="symptom_patient")
    doctor_id = models.ForeignKey(
        "User", on_delete=models.CASCADE, null=True, blank=True,
        db_column="doctor_id", related_name="symptom_publisher")
    s_code = models.CharField(max_length=50)
    s_onset = models.DateTimeField()
    s_severity = models.CharField(max_length=50)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)


class Prescript(models.Model):
    id = models.BigAutoField(help_text="prescript ID", primary_key=True)
    appointment_id = models.ForeignKey(
        "Appointment", on_delete=models.CASCADE, null=True, blank=True,
        db_column="appointment_id")
    patient_id = models.ForeignKey(
        "User", on_delete=models.CASCADE, null=True, blank=True,
        db_column="patient_id", related_name="prescript_patient")
    doctor_id = models.ForeignKey(
        "User", on_delete=models.CASCADE, null=True, blank=True,
        db_column="doctor_id", related_name="prescript_publisher")
    medicine_code = models.CharField(max_length=50)  # 의약품코드
    quantity = models.IntegerField()  # 처방 수량
    medicine_unit = models.CharField(max_length=50)  # 처방 단위
    medicine_begin_time = models.DateTimeField()  # 복용 시작일
    medicine_end_time = models.DateTimeField()  # 복용 종료일
    medicine_dose_unit = models.CharField(max_length=50)  # 복용단위
    medicine_dose = models.IntegerField()  # 복용횟수
    medicine_usage = models.CharField(max_length=50)  # 복용방법
    comment = models.CharField(max_length=500)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)


class UserManager(BaseUserManager):

    def create_user(self, username, name, password, email, address, subject,
                    phone_number):
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(
            username=username,
            name=name,
            email=email,
            address=address,
            subject=subject,
            phone_number=phone_number
        )
        # NOTE: 왜 얘만 따로 뻈지?
        user.set_password(password)

        user.save(using=self._db)
        return user


class User(_User):
    # 기본정보
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    join_date = models.DateTimeField(auto_now_add=True)
    phone_number = PhoneNumberField()
    # 소속을 나타내는 칼럼들
    subject = models.CharField(max_length=50)
    authority = models.IntegerField(default=0)  # 0: 외부, 1: 의사, 2: 관리자

    objects = UserManager()

    REQUIRED_FIELDS = ['alias']

    def __str__(self):
        return self.username

    def create_user(self, username, password, name, email, address, subject,
                    phone_number):
        user = User(
            username=username,
            password=password,
            name=name,
            email=email,
            address=address,
            subject=subject,
            phone_number=phone_number
        )
        user.save()
        return user
