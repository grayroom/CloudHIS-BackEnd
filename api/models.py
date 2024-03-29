from django.db import models

from django.contrib.auth.models import User as _User


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
        "Patient", on_delete=models.CASCADE, null=True, blank=True,
        db_column="patient_id", related_name="patient_ref_id")
    doctor_id = models.ForeignKey(
        "Doctor", on_delete=models.CASCADE, null=True, blank=True,
        db_column="doctor_id", related_name="doctor_ref_id")
    begin_at = models.DateTimeField()
    category = models.CharField(max_length=50)  # 진료, 검사, 수술, 상담
    status = models.CharField(max_length=50)
    preliminary = models.CharField(max_length=5000, null=True, blank=True)
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
    begin_at = models.DateTimeField(null=True, blank=True)
    end_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    diag_type = models.CharField(max_length=50, null=True, blank=True)
    comment = models.CharField(max_length=5000, null=True, blank=True)
    named_entity = models.JSONField(default=dict, null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)


class Symptom(models.Model):
    id = models.BigAutoField(help_text="symptom ID", primary_key=True)
    diagnosis_id = models.ForeignKey(
        "Diagnosis", on_delete=models.CASCADE, null=True, blank=True,
        db_column="diagnosis_id")
    patient_id = models.ForeignKey(
        "User", on_delete=models.CASCADE, null=True, blank=True,
        db_column="patient_id", related_name="symptom_patient")
    doctor_id = models.ForeignKey(
        "User", on_delete=models.CASCADE, null=True, blank=True,
        db_column="doctor_id", related_name="symptom_publisher")
    s_name = models.CharField(max_length=50, null=True, blank=True)

    # NOTE FIXME 아래 3개 필드는 실제 구현에는 필요하지만 아직 데이터 부족으로 미구현
    # null, blank 없애야한다!!!
    s_code = models.CharField(max_length=50, null=True, blank=True)
    s_onset = models.DateTimeField(null=True, blank=True)
    s_severity = models.CharField(max_length=50, null=True, blank=True)

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)


class Prescript(models.Model):
    id = models.BigAutoField(help_text="prescript ID", primary_key=True)
    diagnosis_id = models.ForeignKey(
        "Diagnosis", on_delete=models.CASCADE, null=True, blank=True,
        db_column="diagnosis_id")
    patient_id = models.ForeignKey(
        "User", on_delete=models.CASCADE, null=True, blank=True,
        db_column="patient_id", related_name="prescript_patient")
    doctor_id = models.ForeignKey(
        "User", on_delete=models.CASCADE, null=True, blank=True,
        db_column="doctor_id", related_name="prescript_publisher")
    medicine_name = models.CharField(
        max_length=50, null=True, blank=True)  # 의약품명

    # NOTE FIXME 아래 9개 필드는 실제 구현에는 필요하지만 아직 데이터 부족으로 미구현
    # null, blank 없애야한다!!!
    medicine_code = models.CharField(
        max_length=50, null=True, blank=True)  # 의약품코드
    quantity = models.IntegerField(null=True, blank=True)  # 처방 수량
    medicine_unit = models.CharField(
        max_length=50, null=True, blank=True)  # 처방 단위
    medicine_begin_time = models.DateTimeField(null=True, blank=True)  # 복용 시작일
    medicine_end_time = models.DateTimeField(null=True, blank=True)  # 복용 종료일
    medicine_dose_unit = models.CharField(
        max_length=50, null=True, blank=True)  # 복용단위
    medicine_dose = models.IntegerField(null=True, blank=True)  # 복용횟수
    medicine_usage = models.CharField(
        max_length=50, null=True, blank=True)  # 복용방법
    comment = models.CharField(max_length=500, null=True, blank=True)

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class User(models.Model):
    user_ptr = models.OneToOneField(
        AuthUser, models.DO_NOTHING, primary_key=True)
    name = models.CharField(max_length=50)
    dob = models.DateField()
    sex = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    join_date = models.DateTimeField()
    phone_number = models.CharField(max_length=128)
    authority = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'auths_user'

# NOTE: 이하는 auth 에서 구현한 USER에 대한것


class Doctor(User):
    user_idx = models.OneToOneField(User, on_delete=models.CASCADE,
                                    parent_link=True, primary_key=True)
    subject = models.CharField(max_length=50, null=True, default=None)
    position = models.CharField(max_length=50, null=True, default=None)
    room = models.CharField(max_length=50, null=True, default=None)
    dept_idx = models.IntegerField(null=True, default=None)
    sup_idx = models.IntegerField(null=True, default=None)

    def __str__(self):
        return self.username

    class Meta:
        managed = False
        db_table = 'auths_doctor'


class Patient(User):
    user_idx = models.OneToOneField(User, on_delete=models.CASCADE,
                                    parent_link=True, primary_key=True)
    doc_idx = models.IntegerField(default=0)
    is_admission = models.BooleanField(default=False)
    room = models.CharField(max_length=50, null=True, default=None)

    def __str__(self):
        return self.username

    class Meta:
        managed = False
        db_table = 'auths_patient'


class NerHistory(models.Model):
    id = models.BigIntegerField(help_text="ner history ID", primary_key=True)
    diag_id = models.ForeignKey(
        "Diagnosis", on_delete=models.CASCADE, null=True, blank=True,
        db_column="diag_id")
    patient_id = models.ForeignKey(
        "User", on_delete=models.CASCADE, null=True, blank=True,
        db_column="patient_id", related_name="ner_patient")
    doctor_id = models.ForeignKey(
        "User", on_delete=models.CASCADE, null=True, blank=True,
        db_column="doctor_id", related_name="ner_publisher")
    target_text = models.TextField(null=True, blank=True)
    ner_result = models.JSONField(default=dict, null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
