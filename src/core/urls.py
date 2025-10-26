# core/urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
# Import your views
from . import views

urlpatterns = [
    # Frontend Pages
    path('', views.IndexView.as_view(), name='index'),
    path('login/', views.LoginPageView.as_view(), name='login'),
    path('register/', views.RegisterPageView.as_view(), name='register'),
    path('dashboard/', views.DashboardPageView.as_view(), name='dashboard'),
    path('forgot-password/', views.ForgotPasswordPageView.as_view(), name='forgot_password'),
    path('reset-password/', views.ResetPasswordPageView.as_view(), name='reset_password'),
    path('profile/', views.ProfilePageView.as_view(), name='profile'),
    
    # API Endpoints
    path('api/auth/login/', views.UserLoginView.as_view(), name='api_login'),
    path('api/auth/logout/', views.UserLogoutView.as_view(), name='api_logout'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='api_token_refresh'),
    path('api/auth/register/', views.UserRegisterView.as_view(), name='api_register'),
    path('api/auth/complete-registration/', views.CompleteRegistrationView.as_view(), name='api_complete_registration'),
    path('api/auth/verify/request/', views.VerificationRequestView.as_view(), name='api_verification_request'),
    path('api/auth/verify/', views.VerifyUserView.as_view(), name='api_verify_user'),
    path('api/auth/verify/status/', views.VerificationStatusView.as_view(), name='api_verification_status'),
    path('api/auth/forgot-password/', views.ForgotPasswordView.as_view(), name='api_forgot_password'),
    path('api/auth/password-reset/request/', views.ForgotPasswordView.as_view(), name='api_password_reset_request'),
    path('api/auth/password-reset/confirm/', views.PasswordResetConfirmView.as_view(), name='api_password_reset_confirm'),
    path('api/auth/dashboard/', views.UserDashboardView.as_view(), name='api_dashboard'),
    path('api/auth/update-profile/', views.UpdateProfileView.as_view(), name='api_update_profile'),
    path('api/auth/change-password/', views.ChangePasswordView.as_view(), name='api_change_password'),
    path('api/auth/contact-commissioner/', views.ContactCommissionerView.as_view(), name='api_contact_commissioner'),
    
    # Reference data endpoints for dropdowns
    path('api/states/', views.StateListView.as_view(), name='api_states'),
    path('api/courses/', views.CourseListView.as_view(), name='api_courses'),
]