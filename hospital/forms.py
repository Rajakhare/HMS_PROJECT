from django import forms
from .models import admin_model, CustomUser, doctor, Specialization, patient, Appointment, Page, Report


class AdminForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)  

    class Meta:
        model = admin_model
        fields = ['name', 'email', 'title', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
         # Create a new user for CustomUser and set the password using set_password
        password = self.cleaned_data.get('password')
        if password:
            # Create a new CustomUser instance
            user = CustomUser.objects.create(
                email=self.cleaned_data['email'],
                username=self.cleaned_data['email'],  # Or any unique username field
                user_type='admin',  # Or assign the appropriate user type
            )
            user.set_password(password)  # This automatically hashes the password
            user.save()
            # Now create the admin model instance, linked to the CustomUser
            admin_instance = super().save(commit=False)
            admin_instance.user = user  # Link the CustomUser to the admin model
            admin_instance.name = self.cleaned_data['name']  # Set the name field in admin_model
            if commit:
                admin_instance.save()
            return admin_instance
        return super().save(commit=commit)

class LoginForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=255, widget=forms.EmailInput(attrs={'placeholder': 'Enter your email', 'class': 'form-control',}))
    
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}))
    # password = forms.CharField(widget=forms.PasswordInput)

class DoctorSignUpForm(forms.ModelForm): 
    
    first_name = forms.CharField(label="first_name", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first_name'}))
    last_name = forms.CharField(label="last_name", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last_name'}))
    email = forms.EmailField(label="email", max_length=255, widget=forms.EmailInput(attrs={'placeholder': 'Enter your email', 'class': 'form-control',}))
    mobile_number = forms.CharField(label="mobile_number", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter mobile number'}))
    fees = forms.CharField(label="fees", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter fees'}))
    specialization = forms.ModelChoiceField(queryset=Specialization.objects.all(), label="Select Specialization")
    password = forms.CharField(label="password", max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}))    
    class Meta:
        model  = CustomUser
        fields = ['username', 'email']

        
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter username'}),
            'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Enter email'}),
            
           
        }

        def clean(self):
            cleaned_data = super().clean()
            return cleaned_data

    def save(self, commit=True):
        password = self.cleaned_data.get('password')
        if password:
            # Create a new CustomUser instance
            user = CustomUser.objects.create(
                email=self.cleaned_data['email'],
                username=self.cleaned_data['email'],  # Or any unique username field
                user_type='doctor',  # Or assign the appropriate user type
            )
            user.set_password(password)  # This automatically hashes the password
            user.save()

          # Now create the admin model instance, linked to the CustomUser
            admin_instance = super().save(commit=False)
            admin_instance.user = user  # Link the CustomUser to the admin model
            admin_instance.first_name = self.cleaned_data['first_name']  # Set the name field in admin_model
            if commit:
                admin_instance.save()

            return admin_instance

        return super().save(commit=commit)


class DoctorLoginForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=255, widget=forms.EmailInput(attrs={'placeholder': 'Enter your email', 'class': 'form-control',}))
    
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}))


class SpecializationForm(forms.ModelForm):
    class Meta:
        model = Specialization
        fields = '__all__'


        
        

class PatientSignUpForm(forms.ModelForm): 
    
    first_name = forms.CharField(label="first_name", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first_name'}))
    last_name = forms.CharField(label="last_name", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last_name'}))
    email = forms.EmailField(label="email", max_length=255, widget=forms.EmailInput(attrs={'placeholder': 'Enter your email', 'class': 'form-control',}))
    gender = forms.CharField(label="gender", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter gender'}))
    mobile_number = forms.CharField(label="mobile_number", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter mobile number'}))
    address = forms.CharField(max_length=200)
    password = forms.CharField(label="password", max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}))   

    class Meta:
        model  = CustomUser
        fields = ['username', 'email']

        
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter username'}),
            'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Enter email'}),  
        }

        def clean(self):
            cleaned_data = super().clean()
            return cleaned_data

    def save(self, commit=True):
        password = self.cleaned_data.get('password')
        if password:
            # Create a new CustomUser instance
            user = CustomUser.objects.create(
                email=self.cleaned_data['email'],
                username=self.cleaned_data['email'],  # Or any unique username field
                user_type='patient',  # Or assign the appropriate user type
            )
            user.set_password(password)  # This automatically hashes the password
            user.save()

          # Now create the admin model instance, linked to the CustomUser
            admin_instance = super().save(commit=False)
            admin_instance.user = user  # Link the CustomUser to the admin model
            admin_instance.first_name = self.cleaned_data['first_name']  # Set the name field in admin_model
            if commit:
                admin_instance.save()

            return admin_instance

        return super().save(commit=commit)
    

class PatientLoginForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=255, widget=forms.EmailInput(attrs={'placeholder': 'Enter your email', 'class': 'form-control',}))
    
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}))


class PatientUpdateForm(forms.ModelForm):
    class Meta:
        model = patient
        fields = ['first_name', 'last_name', 'gender', 'email', 'mobile_number', 'address', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
    
    def clean_password(self):
        password = self.cleaned_data.get("password")
        if password:
            return password
        return None


class BookAppointmentForm(forms.ModelForm):
    date_of_appointment = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    time_of_appointment = forms.TimeField(widget=forms.TimeInput(attrs={'type':'time'}))

    class Meta:
        model = Appointment
        fields = ['spec_id', 'doctor_id', 'date_of_appointment', 'time_of_appointment', 'additional_msg', 'status']

        def __init__(self, *args, **kwargs):
            super(BookAppointmentForm, self).__init__(*args, **kwargs)
            self.fields['doctor_id'].queryset = doctor.objects.none()

            if 'spec_id' in self.data:
                try:
                    spec_id = int(self.data.get('spec_id'))
                    self.fields['doctor_id'].queryset = doctor.objects.filter(Specialization=spec_id)
                except(ValueError, TypeError):
                    pass
            elif self.instance.pk:
                self.fields['doctor_id'].queryset = self.instance.spec_id.doctor.set.all()
            

class UpdateAppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['status', 'remark']
        
        widgets = {
            'status': forms.Select(choices=Appointment.STATUS_CHOICES, attrs={'class': 'form-control'}),
            'remark': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

        


class ContactForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ['full_name', 'email', 'message']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your message', 'rows': 4}),
        }


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['patient', 'diagnosis', 'prescription']
        widgets = {
            'diagnosis': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'prescription': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'patient': forms.Select(attrs={'class': 'form-control'}),
        }
