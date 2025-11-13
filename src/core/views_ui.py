# core/views_ui.py
# Function-based views for Django session-based UI
import logging
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import User, CollegeData, State, Course
from election.models import VoterToken, Election

logger = logging.getLogger(__name__)


def home(request):
    """Home page view."""
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    return render(request, 'core/home.html')


@require_http_methods(["GET", "POST"])
def login_view(request):
    """Login view with Django session authentication."""
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    
    if request.method == 'POST':
        registration_number = request.POST.get('registration_number')
        password = request.POST.get('password')
        
        # Authenticate using the custom backend
        user = authenticate(request, registration_number=registration_number, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name}!')
            return redirect('core:dashboard')
        else:
            messages.error(request, 'Invalid registration number or password.')
    
    return render(request, 'core/login.html')


@login_required
def logout_view(request):
    """Logout view."""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('core:login')


@require_http_methods(["GET", "POST"])
def register_view(request):
    """Two-step registration view for new users.
    Step 1: Verify registration number in college data
    Step 2: Complete registration with email, password, state, etc.
    """
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    
    if request.method == 'POST':
        step = request.POST.get('step', '1')
        
        # STEP 1: Check registration number in college data
        if step == '1':
            registration_number = request.POST.get('registration_number', '').strip()
            
            if not registration_number:
                messages.error(request, 'Registration number is required.')
                return render(request, 'core/register.html', {'step': 1})
            
            try:
                # Check if college data exists and is not used
                college_data = CollegeData.objects.get(
                    registration_number=registration_number,
                    is_used=False
                )
                
                # Check if user already exists
                if User.objects.filter(registration_number=registration_number).exists():
                    messages.error(request, 'Registration number already registered.')
                    return render(request, 'core/register.html', {'step': 1})
                
                # College data found, proceed to step 2 with pre-filled info
                context = {
                    'step': 2,
                    'registration_number': college_data.registration_number,
                    'first_name': college_data.first_name,
                    'last_name': college_data.last_name,
                    'gender': college_data.gender,
                    'suggested_email': college_data.email if college_data.email else '',
                    'course_id': college_data.course.id if college_data.course else None,
                    'states': State.objects.all(),
                    'courses': Course.objects.all()
                }
                return render(request, 'core/register.html', context)
                
            except CollegeData.DoesNotExist:
                messages.error(request, 'Registration number not found or already used.')
                return render(request, 'core/register.html', {'step': 1})
        
        # STEP 2: Complete registration
        elif step == '2':
            registration_number = request.POST.get('registration_number')
            email = request.POST.get('email')
            password = request.POST.get('password')
            password_confirm = request.POST.get('password_confirm')
            state_id = request.POST.get('state')
            course_id = request.POST.get('course')
            
            # Validate all fields
            if not all([registration_number, email, password, password_confirm, state_id, course_id]):
                messages.error(request, 'All fields are required.')
                college_data = CollegeData.objects.get(registration_number=registration_number)
                context = {
                    'step': 2,
                    'registration_number': registration_number,
                    'first_name': college_data.first_name,
                    'last_name': college_data.last_name,
                    'gender': college_data.gender,
                    'states': State.objects.all(),
                    'courses': Course.objects.all()
                }
                return render(request, 'core/register.html', context)
            
            if password != password_confirm:
                messages.error(request, 'Passwords do not match.')
                college_data = CollegeData.objects.get(registration_number=registration_number)
                context = {
                    'step': 2,
                    'registration_number': registration_number,
                    'first_name': college_data.first_name,
                    'last_name': college_data.last_name,
                    'gender': college_data.gender,
                    'states': State.objects.all(),
                    'courses': Course.objects.all()
                }
                return render(request, 'core/register.html', context)
            
            try:
                # Verify college data still valid
                college_data = CollegeData.objects.get(
                    registration_number=registration_number,
                    is_used=False
                )
                
                # Check email not already used
                if User.objects.filter(email=email.lower()).exists():
                    messages.error(request, 'Email already registered.')
                    context = {
                        'step': 2,
                        'registration_number': registration_number,
                        'first_name': college_data.first_name,
                        'last_name': college_data.last_name,
                        'gender': college_data.gender,
                        'states': State.objects.all(),
                        'courses': Course.objects.all()
                    }
                    return render(request, 'core/register.html', context)
                
                # Get state and course
                state = State.objects.get(id=state_id)
                course = Course.objects.get(id=course_id)
                
                # Create user from college data
                user, _ = User.objects.create_from_college_data(college_data.id)
                
                # Update user with provided details
                user.email = email.lower()
                user.state = state
                user.course = course
                user.set_password(password)
                user.save()
                
                # Mark college data as used
                college_data.is_used = True
                college_data.save()
                
                messages.success(request, 'Registration successful! Please log in.')
                return redirect('core:login')
                
            except CollegeData.DoesNotExist:
                messages.error(request, 'Registration number not found or already used.')
                return render(request, 'core/register.html', {'step': 1})
            except State.DoesNotExist:
                messages.error(request, 'Invalid state selected.')
                return render(request, 'core/register.html', {'step': 1})
            except Course.DoesNotExist:
                messages.error(request, 'Invalid course selected.')
                return render(request, 'core/register.html', {'step': 1})
            except Exception as e:
                logger.error(f"Registration error: {str(e)}")
                messages.error(request, 'Registration failed. Please try again.')
                return render(request, 'core/register.html', {'step': 1})
    
    # GET request - show step 1
    return render(request, 'core/register.html', {'step': 1})


@login_required
def dashboard_view(request):
    """User dashboard view."""
    user = request.user
    
    # Get user's voting tokens
    tokens = VoterToken.objects.filter(user=user).select_related(
        'election', 'election_level'
    )
    
    # Get active elections
    active_elections = Election.objects.filter(is_active=True)
    
    context = {
        'user': user,
        'voting_tokens': tokens,
        'active_elections': active_elections,
    }
    
    return render(request, 'core/dashboard.html', context)
