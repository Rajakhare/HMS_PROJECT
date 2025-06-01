from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.hashers import make_password

# Create your models here.
class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = CustomUser(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, password=None, **extra_field):
        return self._create_user(email, password, **extra_field)
    

# Custom User Model
class CustomUser(AbstractUser):
    USER = (
        ('admin','admin'),
        ('doctor','doctor'),
        ('patient','patient')
    )
    username = models.CharField(max_length=150, unique=True, blank=False, null=False)
    email = models.EmailField(unique=True)  # Use email for authentication
    user_type = models.CharField(max_length=20, choices=USER, default=None)

    USERNAME_FIELD = 'email'  # Use email as the unique identifier
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email}"

class admin_model(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    title = models.CharField(max_length=255)
    password = models.CharField(max_length=128)

    USERNAME_FIELD = 'email'  # Use email as the unique identifier
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.user.email} (Admin)"


# Specilization 
class Specialization(models.Model):
    s_name = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self): 
        return self.s_name
    

# Doctor Model View
class doctor(models.Model):
    username = models.OneToOneField(CustomUser, on_delete=models.CASCADE, max_length=100, related_name="doctor", null=True)
    first_name = models.CharField(max_length=100, default=None)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=220)
    mobile_number = models.CharField(max_length=100)
    fees = models.DecimalField(max_digits=6,decimal_places=2, max_length=100, default=None)
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE)
    password = models.CharField(max_length=100)
    

    USERNAME_FIELD = 'email'  # Use email as the unique identifier
    REQUIRED_FIELDS = []

    def __str__(self):
        return f" Dr.{self.first_name} {self.last_name} (doctor)"
    

# Doctor Model View
class patient(models.Model):
    username = models.OneToOneField(CustomUser, on_delete=models.CASCADE, max_length=100, related_name="patient", null=True)
    first_name = models.CharField(max_length=100, default=None)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=100, choices= [('M','Male'), ('F','Female'), ('O','Others')])
    email = models.EmailField(max_length=220)
    mobile_number = models.CharField(max_length=100)
    address = models.TextField()
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'  # Use email as the unique identifier
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.first_name} {self.last_name} (patient)"
    


class Appointment(models.Model):
    appointmentnumber = models.AutoField(primary_key=True, unique=True)
    spec_id = models.ForeignKey(Specialization, on_delete=models.CASCADE,default=0)
    pat_id = models.ForeignKey(patient, on_delete=models.CASCADE,related_name="appointment")    
    date_of_appointment = models.CharField(max_length=250)
    time_of_appointment = models.CharField(max_length=250)
    doctor_id = models.ForeignKey(doctor, on_delete=models.CASCADE, related_name="appointment")
    additional_msg = models.TextField(blank=True)
    remark = models.CharField(max_length=250,default=0)
    
    STATUS_CHOICES = [
        ('new', 'New'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    status = models.CharField(max_length=200, choices=STATUS_CHOICES)
   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Appointment {self.appointmentnumber} - {self.pat_id} {self.pat_id.first_name} {self.pat_id.last_name} {self.doctor_id.first_name} {self.doctor_id.last_name}"
    
    def get_status_display(self):
        return dict(self.STATUS_CHOICES) [self.status]
    


class Page(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=80)
    message = models.TextField(max_length=200)

    def __str__(self):
        return f"{self.full_name}"


class Report(models.Model):
    patient = models.ForeignKey(patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(doctor, on_delete=models.CASCADE)  # Assuming doctors are users
    diagnosis = models.TextField()
    prescription = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report for {self.patient.first_name} by {self.doctor.first_name} {self.created_at}"