"""
URL configuration for HMS_PROJECT project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from hospital import views

app_name = 'hospital'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.Home, name="home"),
    path('adminsignup/', views.Admin_SignUp, name="adminsignup"),
    path('adminlogin/', views.Admin_Login, name="adminlogin"),
    path('admin_logout/', views.Admin_Logout, name="admin_logout"),
    path('admindashboard/', views.Admin_Dashboard, name="admindashboard"),
    path('doctorsignup/', views.Doctor_SignUp, name="doctorsignup"),
    path('doctorlogin/', views.Doctor_Login, name="doctorlogin"),
    path('doctor_logout/', views.Doctor_Logout, name="doctor_logout"),
    path('doctordashboard/', views.Doctor_Dashboard, name="doctordashboard"),
    path('doctorlist/', views.Doctor_List, name="doctorlist"),
    path('create_report/', views.Create_Report, name="create_report"),
    path('update_appointment_status/<int:appointment_id>/', views.Update_Appointment_Status, name="update_appointment_status"),
    path('specializationlist/', views.specialization_list, name="specializationlist"),
    path('specializationadd/', views.Add_Specialization, name="specialization_add"),
    path('specializationupdate/<int:pk>/', views.Update_Specialization, name="specializationupdate"),
    path('specializationdelete/<int:id>/', views.Delete_Specialization, name="specializationdelete"),
    path('patientregister/', views.Patient_SignUp, name="patientregister"),
    path('patientlogin/', views.Patient_Login, name="patientlogin"),
    path('patient_logout/', views.Patient_Logout, name="patient_logout"),
    path('patientdashboard/', views.Patient_Dashboard, name="patientdashboard"),
    path('patientlist/', views.Patient_List, name="patientlist"),
    path('book_appointment/', views.Book_Appointment, name="book_appointment"),
    path('appointment_history/', views.Appointment_History, name="appointment_history"),
    path('delete_appointment/<int:appointment_id>/', views.Delete_Appointment, name="delete_appointment"),
    path('new_appointment/', views.New_Appointment, name='new_appointment'),
    path('confirmed_appointment/', views.Confirmed_Appointment, name='confirmed_appointment'),
    path('cancelled_appointment/', views.Cancelled_Appointment, name='cancelled_appointment'),
    path('completed_appointment/', views.Completed_Appointment, name='completed_appointment'),
    path('all_appointment/', views.All_Appointment, name='all_appointment'),
    path('our_service/', views.Our_Service, name="our_service"),
    path('doctors/', views.Doctors, name="doctors"),
    path('about/', views.About, name="about"),
    path('contact/', views.Contact, name="contact"),
    path('contact_success/', views.Contact_Success, name="contact_success"),
     path('generate_pdf/<int:report_id>/', views.Generate_Pdf, name='generate_pdf'),
]

