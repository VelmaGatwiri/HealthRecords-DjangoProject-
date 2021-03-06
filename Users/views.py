from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *
from django.shortcuts import render
from django.views.generic import CreateView
from .decorators import *
from MedicalApp.filters import *
from MedicalApp.models import *
import csv
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
pdfmetrics.registerFont(TTFont('VeraIt', 'VeraIt.ttf'))
pdfmetrics.registerFont(TTFont('VeraBI', 'VeraBI.ttf'))


def home(request):
    return render(request, 'Users/Homepage.html')


@login_required
# @allowed_users(allowed_roles=['Patient', 'Doctor'])
def patient(request, pk):
    pat = Patient.objects.get(user_id=pk)

    records = pat.record_set.all().order_by('-Record_Date')

    patientfilter = RecordPatientFilter(request.GET, queryset=records)
    records = patientfilter.qs

    context = {'pat': pat, 'records': records, 'patientfilter': patientfilter}
    return render(request, 'Users/PatientModule.html', context)


@login_required
@allowed_users(allowed_roles=['Admin'])
def admin(request, pk):
    adm = Administrator.objects.get(user_id=pk)
    hos = admin.hospital_set.all().order_by('-Registration_Date')
    context = {'adm': adm, 'hos': hos}
    return render(request, 'Users/AdminModule.html', context)


@login_required
@allowed_users(allowed_roles=['Doctor'])
def doctor(request, pk):
    doct = Doctor.objects.get(user_id=pk)

    records = doct.record_set.all().order_by('-Record_Date')

    myfilter = RecordFilter(request.GET, queryset=records)
    records = myfilter.qs

    context = {'doct': doct, 'records': records, 'myfilter': myfilter}
    return render(request, 'Users/DoctorModule.html', context)


@login_required
# @allowed_users(allowed_roles=['Hospital'])
def hospital(request):
    context = {
        'hos': Hospital.objects.all()
    }
    return render(request, 'Users/HospitalModule.html', context)


def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_doctor:
                login(request, user)
                return redirect('DoctorModule', user.id)
            if user is not None and user.is_administrator:
                login(request, user)
                return redirect('AdminModule', user.id)
            if user is not None and user.is_hospital:
                login(request, user)
                return redirect('HospitalModule', hospital.id)
            else:
                messages.info(request, 'Username or Password is incorrect')
        else:
            messages.info(request, 'Error Validating Forms')

    return render(request, 'Users/StaffLogin.html', {'form': form})


class PatientRegistration(CreateView):
    model = CustomUser
    form_class = PatientRegistrationForm
    template_name = 'Users/PatientRegistration.html'

    def validation(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('HospitalModule')


class DoctorRegistration(CreateView):
    model = CustomUser
    form_class = DoctorRegistrationForm
    template_name = 'Users/DoctorRegistration.html'

    def validation(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('HospitalModule')


class HospitalRegistration(CreateView):
    model = CustomUser
    form_class = HospitalRegistrationForm
    template_name = 'Users/HospitalRegistration.html'
    title = 'Hospital Registration'

    def validation(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')


def user_details(request, pk):
    patients = Patient.objects.get(user_id=pk)
    appointment = patients.appointment_set.filter(Appointment_Status="Pending")

    context = {'patients': patients, 'appointment': appointment}
    return render(request, 'Users/User_Details.html', context)


def doctor_details(request, pk):
    doc = Doctor.objects.get(user_id=pk)
    appointment = doc.appointment_set.filter(Appointment_Status="Pending")

    context = {'doc': doc, 'appointment': appointment}

    return render(request, 'Users/Doctor_Details.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your Profile has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'Users/profile.html', context)


def records_pdf(request):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont('Vera', 4)

    #    lines = [

    #   ]
    record = Record.objects.all()
    lines = []
    for record in record:
        lines.append(record.Patient_ID)
        lines.append(record.Doctor_ID)
        lines.append(record.Hospital_ID)
        lines.append(record.New_Diagnosis)
        lines.append(record.Record_Date)
        lines.append(" ")

    for line in lines:
        textob.textLine(line)

    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='records_Pdf')
