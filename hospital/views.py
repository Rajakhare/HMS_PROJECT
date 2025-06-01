from django.db import IntegrityError
from django.http import Http404, JsonResponse
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .forms import AdminForm, LoginForm, DoctorSignUpForm, DoctorLoginForm, SpecializationForm, PatientSignUpForm, PatientLoginForm, BookAppointmentForm, UpdateAppointmentForm, ContactForm, PatientUpdateForm, ReportForm
from .models import admin_model,CustomUser, doctor, Specialization, patient, Appointment, Report
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


# Home View
def Home(request):
     return render(request, 'home/home.html')

# Admin SignUp View
def Admin_SignUp(request):
    admin_exist = admin_model.objects.filter(title='admin').exists()
    print ("Admin Exist = ", admin_exist)
    if not admin_exist:
        if request.method == 'POST':
            print("Post method")
            form = AdminForm(request.POST)
            print(form)
            if form.is_valid():
                form.save()
                return render(request, 'home/admin_login.html', {'form': form})
            else:
                print("not valid")
                HttpResponse("form is not valid")
        else:
            form = AdminForm() 
        return render(request, 'home/admin_Signup.html', {'form': form})
    else:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                print(email)
                print(password)
                try:
                    user = CustomUser.objects.get(email=email)
                    name = user.admin_model.name if user.user_type == 'admin' else user.username

                    if check_password(password, user.password):
                        login(request, user)
                        if user.user_type == 'admin':
                            print("admin login")
                            name = user.admin_model.name
                            return render(request, 'home/admin_dashboard.html', {'name': name, 'email': user.email})
                        else:
                            return HttpResponse("Not login")
                        
                except CustomUser.DoesNotExist:
                    return HttpResponse("User does not exist")
        else:
            form = LoginForm()
        return render(request, 'home/admin_login.html', {'form': form})
    
    
# Admin Login View
def Admin_Login(request):
    print("Login")
    return render(request, 'home/admin_login.html')

def Admin_Logout(request):
    logout(request)
    return render(request, 'home/admin_login.html')


# Admin Dashboard View
@login_required
def Admin_Dashboard(request):
    user = request.user
    admin_name = user.admin_model.name
    doctor_count = doctor.objects.count()
    patient_count = patient.objects.count()
    specialization_count = Specialization.objects.count()
    
    return render(request, 'home/admin_dashboard.html', {'admin_name':admin_name, 'doctor_count':doctor_count, 'specialization_count':specialization_count, 'patient_count':patient_count})
    

# Doctor SignUp View
def Doctor_SignUp(request):
    if request.method == 'POST':
        fm = DoctorSignUpForm(request.POST)
        if fm.is_valid():
            first_name = fm.cleaned_data.get('first_name')
            last_name = fm.cleaned_data.get('last_name')
            email = fm.cleaned_data.get('email')
            mobile_number = fm.cleaned_data.get('mobile_number')
            fees = fm.cleaned_data.get('fees')
            specialization= fm.cleaned_data.get('specialization')
            password = fm.cleaned_data.get('password')
            user = CustomUser.objects.create(
                    username=email,
                    email=email,
                    password=password,
                    user_type="doctor",
            )
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.mobile_number = mobile_number
            user.fees = fees
            # Fetch specialization
            specialization_obj = Specialization.objects.filter(s_name=specialization).first()
            user.specialization = specialization_obj
            user.set_password(password) 
            user.save()
            # Create Doctor instance
            doctor_instance = doctor.objects.create(
                username=user,  # This links the doctor to the CustomUser
                first_name=first_name,
                last_name=last_name,
                email=email,
                mobile_number=mobile_number,
                fees=fees,
                specialization=specialization,
            )
            doctor_instance.save()
            return render(request, 'home/doctor_register.html', {'form': fm, 'doctors': doctor.objects.all()})
    else:
        fm = DoctorSignUpForm()
    return render(request, 'home/doctor_register.html', {'form': fm, 'doctors': doctor.objects.all()})


# Doctor Login View
def Doctor_Login(request):
    if request.method == 'POST':
        form = DoctorLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, username=email, password=password)  # Use authenticate
            if user is not None:
                if user.user_type == 'doctor':
                    login(request, user)  # Log the user in
                    messages.success(request, "Login successful!")
                    return redirect('/doctordashboard/') # Redirect to the doctor's dashboard

                else:
                    messages.error(request, "Invalid credentials. Please try again.")
                    return render(request, 'home/doctor_login.html', {'form': form})

            else:
                messages.error(request, "Invalid credentials. Please try again.")
                return render(request, 'home/doctor_login.html', {'form': form})
        else:
            return render(request, 'home/doctor_login.html', {'form': form})  # Re-render with form errors

    else:
        form = DoctorLoginForm()
        return render(request, 'home/doctor_login.html', {'form': form})

# Logout View
def Doctor_Logout(request):
    logout(request)
    return redirect('/doctorlogin/')
    
# Doctor Dashboard View
def Doctor_Dashboard(request):
    new_count = Appointment.objects.filter(status="New").count()
    confirmed_count = Appointment.objects.filter(status="Confirmed").count()
    cancelled_count = Appointment.objects.filter(status="Cancelled").count()
    completed_count = Appointment.objects.filter(status="Completed").count()
    total_count = Appointment.objects.all().count()
    
    return render(request, 'home/doctor_dashboard.html', {
        'new_count': new_count,
        'confirmed_count': confirmed_count,
        'cancelled_count': cancelled_count,
        'completed_count': completed_count,
        'total_count': total_count,
        'status': 'new'  # Ensure a valid default status
    })

# Doctor List View
def Doctor_List(request):
    doctorlist = doctor.objects.all()
    return render(request, 'home/doctor_list.html', {'doctorlist':doctorlist})

# Add Specialization View
def Add_Specialization(request):
    if request.method == "POST":
        form = SpecializationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('specializationlist'))
    else:
        form = SpecializationForm()
    return render(request, 'home/specialization_add.html', {'form':form})

# Specialization List View
def specialization_list(request):
    specializations = Specialization.objects.all()
    return render(request, 'home/specialization_list.html', {'specializations':specializations})

def Delete_Specialization(request,id):
    specialization = Specialization.objects.get(id=id)
    if request.method == 'POST':
        specialization.delete()
        messages.success(request,'Record Delete Succeesfully!!!')
        return redirect('specializationlist')
    
    context = {
        'specialization' : specialization
    }
    return render(request, 'home/specialization_delete.html', context)

def Update_Specialization(request,pk):
    specialization = get_object_or_404(Specialization, pk=pk)
    if request.method == 'POST':
        form = SpecializationForm(request.POST, instance=specialization)
        if form.is_valid(): 
            form.save()
            return redirect('specializationlist')
    else:
        form = SpecializationForm(instance=specialization)
    return render(request, 'home/update_specialization.html', {'form':form})


# Doctor SignUp View
def Patient_SignUp(request):
    if request.method == 'POST':
        fm = PatientSignUpForm(request.POST)
        if fm.is_valid():
            first_name = fm.cleaned_data.get('first_name')
            last_name = fm.cleaned_data.get('last_name')
            email = fm.cleaned_data.get('email')
            gender = fm.cleaned_data.get('gender')
            mobile_number = fm.cleaned_data.get('mobile_number')
            address = fm.cleaned_data.get('address')
            password = fm.cleaned_data.get('password')

            user = CustomUser.objects.create_user(
                username=email,
                email=email,
                password=password,
                user_type="patient",
            )
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.gender = gender
            user.address = address
            user.set_password(password) 
            user.save()

            # Create Doctor instance
            patient_instance = patient.objects.create(
                username=user,  # This links the doctor to the CustomUser
                first_name=first_name,
                last_name=last_name,
                email=email,
                mobile_number=mobile_number,
                gender=gender,
                address=address,
            )
            patient_instance.save()
            return render(request, 'home/patient_register.html', {'form': fm, 'patients': patient.objects.all()})
    else:
        fm = PatientSignUpForm()
    return render(request, 'home/patient_register.html', {'form': fm, 'patients': patient.objects.all()})


# Patient Login View
def Patient_Login(request): 
    if request.method == 'POST':
        form = PatientLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, username=email, password=password)  # Use authenticate
            if user is not None:
                if user.user_type == 'patient':
                    login(request, user)  # Log the user in
                    messages.success(request, "Login successful!")
                    return redirect('/patientdashboard/') # Redirect to the doctor's dashboard

                else:
                    messages.error(request, "Invalid credentials. Please try again.")
                    return render(request, 'home/patient_login.html', {'form': form})

            else:
                messages.error(request, "Invalid credentials. Please try again.")
                return render(request, 'home/patient_login.html', {'form': form})
        else:
            return render(request, 'home/patient_login.html', {'form': form})  # Re-render with form errors
    else:
        form = PatientLoginForm()
    return render(request, 'home/patient_login.html', {'form': form})



@login_required
def update_patient(request):
    user_patient = get_object_or_404(patient, username=request.user)
    if request.method == "POST":
        form = PatientUpdateForm(request.POST, instance=user_patient)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = PatientUpdateForm(instance=user_patient)
    return render(request, 'patient_dashboard.html', {'form': form})


def Patient_Logout(request):
    logout(request)
    return redirect('/patientlogin/')


# Patient Dashboard View
def Patient_Dashboard(request):
    first_name = request.user.first_name
    last_name = request.user.last_name
    return render(request,'home/patient_dashboard.html', {'first_name':first_name, 'last_name':last_name})


def Patient_List(request):
    patientlist = patient.objects.all()
    return render(request, 'home/patient_list.html', {'patientlist':patientlist})

# # ✅ Patient Side - Book Appointment
def Book_Appointment(request):
    if request.method == 'POST':
        form = BookAppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.pat_id = request.user.patient  # Assign logged-in patient
            
            Doctor = doctor.objects.first()  # Get the first available doctor instance
            if doctor:
               appointment.doctor_id = Doctor  # ✅ Assign doctor instance, not class
            else:
               return HttpResponse("❌ No doctor available!", status=400)


            # ✅ Assign unique appointment number
            last_appointment = Appointment.objects.order_by('-appointmentnumber').first()
            appointment.appointmentnumber = last_appointment.appointmentnumber + 1 if last_appointment else 1

            appointment.save()
            return redirect('/appointment_history/')
        else:
            print("❌ Form is not valid")
    else:
        form = BookAppointmentForm()
    return render(request, 'home/book_appointment.html', {'form': form})

# # Patient Side Appointment History Section
@login_required
def Appointment_History(request):
    appointments = Appointment.objects.filter(pat_id=request.user.patient)
    return render(request, 'home/appointment_history.html', {'appointments':appointments})

@login_required
def Update_Appointment_Status(request, appointment_id):
    appointment = get_object_or_404(Appointment, appointmentnumber=appointment_id)

    if request.method == 'POST':
        form = UpdateAppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('/doctordashboard/')  # Ensure this URL is correct
    else:
        form = UpdateAppointmentForm(instance=appointment)

    return render(request, 'home/update_appointment.html', {'form': form, 'appointment': appointment})


@login_required
def New_Appointment(request):
    """ Fetch new appointments (status = 'pending') and display them. """
    appointments = Appointment.objects.filter(status='new').select_related('doctor_id', 'pat_id')
    patient_name  = patient.first_name
    doctor_name = doctor.first_name
    if not appointments.exists():
        messages.info(request, "No new appointments available.")
    
    return render(request, 'home/new_appointment.html', {'appointments': appointments, 'patient_name':patient_name, 'doctor_name':doctor_name})

@login_required
def All_Appointment(request):
    """ Fetch all appointments for display. """
    appointments = Appointment.objects.select_related('doctor_id', 'pat_id').all()
    
    if not appointments.exists():
        messages.info(request, "No appointments available.")
    
    return render(request, 'home/all_appointment.html', {'appointments': appointments})

@login_required
def Confirmed_Appointment(request):
    """ Fetch confirmed appointments (status = 'confirmed'). """
    appointments = Appointment.objects.filter(status='confirmed').select_related('doctor_id', 'pat_id')
    
    if not appointments.exists():
        messages.info(request, "No confirmed appointments available.")
    
    return render(request, 'home/confirmed_appointment.html', {'appointments': appointments})

@login_required
def Cancelled_Appointment(request):
    """ Fetch cancelled appointments (status = 'cancelled'). """
    appointments = Appointment.objects.filter(status='cancelled').select_related('doctor_id', 'pat_id')
    
    if not appointments.exists():
        messages.info(request, "No cancelled appointments available.")
    
    return render(request, 'home/cancelled_appointment.html', {'appointments': appointments})

@login_required
def Completed_Appointment(request):
    """ Fetch completed appointments (status = 'completed'). """
    appointments = Appointment.objects.filter(status='completed').select_related('doctor_id', 'pat_id')
    
    if not appointments.exists():
        messages.info(request, "No completed appointments available.")
    
    return render(request, 'home/completed_appointment.html', {'appointments': appointments})

@login_required
def Delete_Appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, appointmentnumber=appointment_id)

    if request.method == 'POST':
        appointment.delete()
        messages.success(request, "Appointment deleted successfully!")
        return redirect('/appointment_history/')

    return render(request, 'home/confirm_delete.html', {'appointment': appointment})

def Create_Report(request):
    report=None
    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
        
            report = form.save()
            return redirect('/generate_pdf/', report_id=report.id)  # Redirect to PDF
    else:
        form = ReportForm()
    
    return render(request, 'home/create_report.html', {'form': form, 'report': report})  # Pass report as None



def Generate_Pdf(request, report_id):
    print("Generating PDF for report ID:", report_id)  # Debugging
    report = Report.objects.get(report_id=report_id)  # Fetch report data
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="report_{report_id.report_id}.pdf"'

    pdf = canvas.Canvas(response, pagesize=letter)
    pdf.setFont("Helvetica", 12)

    # Title
    pdf.drawString(200, 750, "Patient Report")
    pdf.line(200, 745, 400, 745)  # Line under title

    # Patient Details
    pdf.drawString(50, 700, f"Patient Name: {report.patient.first_name}")
    pdf.drawString(50, 680, f"Age: {report.age}")
    pdf.drawString(50, 660, f"Gender: {report.gender}")
    pdf.drawString(50, 640, f"Diagnosis: {report.diagnosis}")
    pdf.drawString(50, 620, f"Prescription: {report.prescription}")
    pdf.drawString(50, 600, f"Notes: {report.notes}")

    pdf.save()
    return response


def Our_Service(request):
    return render(request, 'home/our_service.html')


# Doctors List View
def Doctors(request):
    return render(request, 'home/doctors.html')

# About View
def About(request):
     return render(request, 'home/about.html')

def Contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/contact_success/')  # Redirect to a success page (Create one)
    else:
        form = ContactForm()
    return render(request, 'home/contact.html', {'form': form})

def Contact_Success(request):
    return render(request, 'home/contact_success.html')
