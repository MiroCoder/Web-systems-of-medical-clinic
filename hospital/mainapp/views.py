from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import ScheduleForm, SignUpForm, VisitForm
from .models import MedicalRecordModel, ProfileModel, ScheduleModel, VisitModel


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.email = form.cleaned_data.get("email")
            user.save()
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect("home")
    else:
        form = SignUpForm()
    return render(request, "signup.html", {"form": form})


@login_required
def profile_view(request):
    user = request.user
    try:
        user_profile = ProfileModel.objects.get(user=user)
        medical_record = MedicalRecordModel.objects.get(patient=user_profile)
    except ProfileModel.DoesNotExist:
        return HttpResponse("Profile does not exist.", status=404)
    except MedicalRecordModel.DoesNotExist:
        return HttpResponse("Medical record does not exist.", status=404)

    context = {
        "user": user,
        "profile": user_profile,
        "medical_record": medical_record,
        "additional_info": {
            "full_name": user_profile.full_name,
            "birth_date": user_profile.birth_date,
            "gender": user_profile.get_gender_display(),
            "location": user_profile.location,
            "contact_number": user_profile.contact_number,
        },
    }
    return render(request, "profile.html", context)


def index(request):
    return render(request, "index.html")


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("index")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


@login_required
def appointment(request):
    user_profile = request.user.profilemodel

    if request.method == "POST":
        form = VisitForm(request.POST, user=request.user)
        if form.is_valid():
            visit = form.save(commit=False)
            visit.patient = user_profile
            visit.save()
            return redirect("appointment_records")
    else:
        form = VisitForm(user=request.user)

    return render(request, "appointment.html", {"form": form})


def contacts(request):
    return render(request, "contacts.html")


@login_required
def appointment_records(request):
    user_profile = request.user.profilemodel

    if request.method == "POST":
        if "delete_visit" in request.POST:
            visit_id = request.POST.get("visit_id")
            visit = VisitModel.objects.get(id=visit_id, patient=user_profile)
            visit.delete()
            return redirect("appointment_records")

        form = VisitForm(request.POST, user=request.user)
        if form.is_valid():
            visit = form.save(commit=False)
            visit.patient = user_profile
            visit.save()
            return redirect("appointment_records")
    else:
        form = VisitForm(user=request.user)

    visits = VisitModel.objects.filter(patient=user_profile)
    return render(request, "appointment_records.html", {"form": form, "visits": visits})


def doctors(request):
    return render(request, "doctors.html")


def about_us(request):
    return render(request, "about_us.html")


def schedule_view(request):
    if request.method == "POST":
        form = ScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("schedule")
    else:
        form = ScheduleForm()

    schedules = ScheduleModel.objects.all()
    return render(request, "schedule.html", {"form": form, "schedules": schedules})
