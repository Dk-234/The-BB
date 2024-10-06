from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.db import IntegrityError
from django.contrib.auth.forms import AuthenticationForm


# Custom Registration Form
class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='First name')
    last_name = forms.CharField(max_length=30, required=True, help_text='Last name')
    email = forms.EmailField(max_length=254, required=True, help_text='Valid email address')
    student_id = forms.IntegerField(required=True, help_text='Enter your KL student ID')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'student_id', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        student_id = self.cleaned_data['student_id']
        if commit:
            user.save()
            try:
                Profile.objects.create(user=user, student_id=student_id)
            except IntegrityError:
                user.delete()  # Rollback user creation if the student ID is not unique
                raise forms.ValidationError(f"Student ID {student_id} is already exists. Please enter a unique ID.")
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class RegistrationForm(UserCreationForm):
    id_number = forms.IntegerField(label="ID Number", required=True, help_text="Please enter your KL ID number.")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'id_number']

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        id_number = self.cleaned_data.get('id_number')

        if commit:
            user.save()
            # Create or update the associated UserProfile with the ID number
            Profile.objects.create(user=user, id_number=id_number)

        return user

