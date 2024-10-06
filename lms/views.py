from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import LoginForm
from .forms import RegistrationForm
from .models import Profile
from django.http import HttpResponse
from django.urls import reverse
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import user_passes_test
import requests
import json
import time
from django.http import JsonResponse


# Define your API Key here
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmFwcGVhci5pbiIsImF1ZCI6Imh0dHBzOi8vYXBpLmFwcGVhci5pbi92MSIsImV4cCI6OTAwNzE5OTI1NDc0MDk5MSwiaWF0IjoxNzI3MTYwNjY1LCJvcmdhbml6YXRpb25JZCI6MjcyMjM0LCJqdGkiOiI2M2ZmNTQ5Zi00MmJkLTQwMzYtYmUwOC03MmQyYjBiM2QyMTgifQ.kWTqgv3irYGJdyCIigGS8daqfjuKWaU217vBLrHpZn0"


def home(request):
    return render(request, 'lms/base.html')  # Now this renders the main page
# Registration View


def register(request):
    username = request.GET.get('username', '')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Save the new user and profile
            form.save()
            return redirect('login')  # Redirect to login or another appropriate page
    else:
        form = RegistrationForm(initial={'username': username})
    return render(request, 'lms/register.html', {'form': form})


def manage_users(request):
    users = User.objects.all()
    return render(request, 'lms/manage_users.html', {'users': users})


def user_redirect(request):
    user = request.user
    if user.is_admin:
        return redirect('admin_dashboard')
    else:
        return redirect('user_dashboard')


# Login View
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            # Redirect to role selection page after successful login
            return user_redirect('role_selection')
        else:
            return render(request, 'lms/login.html', {'error': 'Invalid credentials'})

    return render(request, 'lms/login.html')


@login_required
def role_selection(request):
    return render(request, 'lms/role_selection.html')


def logout_view(request):
    logout(request)
    return render(request, 'lms/logout_page.html')


# Dashboard for Students
@login_required
def learner_dashboard(request):
    return render(request, 'lms/learner_dashboard.html')  # Redirect to login if not authenticated


# Dashboard for Teachers
@login_required
def mentor_dashboard(request):

    return render(request, 'lms/mentor_dashboard.html')  # Redirect to login if not authenticated


def create_meeting():
    api_url = "https://api.whereby.dev/v1/meetings"
    data = {
        "endDate": "2099-02-18T14:23:00.000Z",
        "fields": ["hostRoomUrl", "roomUrl"],
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    response = requests.post(api_url, headers=headers, json=data)

    if response.status_code == 201:  # HTTP 201 means the meeting was successfully created
        meeting_data = response.json()
        host_room_url = meeting_data.get("hostRoomUrl")
        room_url = meeting_data.get("roomUrl")
        return room_url, host_room_url
    else:
        return None, None


def start_mentoring(request):
    room_url, host_room_url = create_meeting()

    if room_url and host_room_url:
        # Store both URLs in the session so we can access them later
        request.session['room_url'] = room_url
        request.session['host_room_url'] = host_room_url

        return render(request, 'lms/start_mentoring.html', {'host_room_url': host_room_url})
    else:
        return render(request, 'lms/error.html', {'message': 'Could not create the meeting.'})


def start_learning(request):
    room_url = request.session.get('room_url')

    if room_url:
        return render(request, 'lms/start_learning.html', {'room_url': room_url})
    else:
        return render(request, 'lms/waiting_for_host.html', {'message': 'Waiting for the mentor to start the meeting.'})


# Dashboard for Admins
@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    # You can fetch admin-specific data here
    return render(request, 'lms/admin_dashboard.html')


# To store timer start time in seconds (UNIX timestamp)
def start_timer(request):
    request.session['timer_start'] = time.time()  # Save the start time in the session
    return JsonResponse({'status': 'Timer started'})


# To get the current timer state
def get_timer(request):
    start_time = request.session.get('timer_start', None)
    if start_time:
        elapsed_time = int(time.time() - start_time)  # Calculate elapsed seconds
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        return JsonResponse({'minutes': minutes, 'seconds': seconds})
    return JsonResponse({'minutes': 0, 'seconds': 0})


@login_required
def subject_page(request, subject_name):
    # Logic to handle the subject page based on subject_name
    context = {'subject_name': subject_name}
    return render(request, 'lms/subject_page.html', context)
















