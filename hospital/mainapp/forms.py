from collections import Counter

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Case, When

from .models import AppointmentModel, DoctorModel, ProfileModel, ScheduleModel, VisitModel


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class AppointmentForm(forms.ModelForm):
    date = forms.DateField(label="Date", widget=forms.widgets.DateInput(attrs={"type": "date"}))
    doctor = forms.ModelChoiceField(label="Doctor", queryset=DoctorModel.objects.all())

    class Meta:
        model = VisitModel
        fields = ["patient", "visit_date", "doctor", "reason"]
        labels = {
            "patient": "Patient",
            "date": "Date",
            "doctor": "Doctor",
            "reason": "Reason",
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        self.fields["doctor"].queryset = DoctorModel.objects.all()
        if user:
            self.fields["patient"].queryset = ProfileModel.objects.filter(user=user)


class PatientForm(forms.ModelForm):
    patient_name = forms.ModelChoiceField(label="Patient", queryset=ProfileModel.objects.all())
    date = forms.DateField(label="Date")
    doctor = forms.ModelChoiceField(label="Doctor", queryset=DoctorModel.objects.all())

    class Meta:
        model = AppointmentModel
        fields = ["patient_name", "date", "doctor"]
        labels = {
            "patient_name": "Patient",
            "date": "Date",
            "doctor": "Doctor",
        }


class LoginForm(forms.Form):
    username = forms.CharField(label="User name")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


class ScheduleForm(forms.ModelForm):
    day_of_week = forms.ChoiceField(
        choices=(
            ("Monday", "Monday"),
            ("Tuesday", "Tuesday"),
            ("Wednesday", "Wednesday"),
            ("Thursday", "Thursday"),
            ("Friday", "Friday"),
            ("Saturday", "Saturday"),
            ("Sunday", "Sunday"),
        ),
        label="Day of week",
    )
    doctors = forms.ModelMultipleChoiceField(queryset=DoctorModel.objects.all(), label="Doctors")
    start_time = forms.TimeField(widget=forms.TimeInput(attrs={"type": "time"}), label="Start")
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={"type": "time"}), label="End")

    class Meta:
        model = ScheduleModel
        fields = ["day_of_week", "doctors", "start_time", "end_time"]


class VisitForm(forms.ModelForm):
    visit_date = forms.DateField(label="Visit date", widget=forms.widgets.DateInput(attrs={"type": "date"}))
    visit_time = forms.TimeField(label="Visit time", widget=forms.widgets.TimeInput(attrs={"type": "time"}))

    class Meta:
        model = VisitModel
        fields = ["visit_date", "visit_time", "patient", "doctor", "reason"]
        labels = {
            "visit_date": "Visit date",
            "visit_time": "Time",
            "patient": "Patient",
            "doctor": "Doctor",
            "reason": "Reason",
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user:
            user_profile = user.profilemodel
            visits = VisitModel.objects.filter(patient=user_profile)
            doctor_counts = Counter(visit.doctor for visit in visits if visit.doctor)
            sorted_doctors = sorted(doctor_counts, key=lambda doctor: -doctor_counts[doctor])
            sorted_doctor_ids = [doctor.id for doctor in sorted_doctors]

            remaining_doctors = DoctorModel.objects.exclude(id__in=sorted_doctor_ids)
            preferred_doctors = DoctorModel.objects.filter(id__in=sorted_doctor_ids)
            self.fields["doctor"].queryset = preferred_doctors | remaining_doctors

            self.fields["patient"].initial = user_profile
            self.fields["patient"].queryset = ProfileModel.objects.filter(user=user)
            self.fields["patient"].widget = forms.HiddenInput()
            self.fields["patient"].disabled = True
