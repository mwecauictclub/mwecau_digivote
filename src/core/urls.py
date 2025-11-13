# core/urls.py
from django.urls import path
from .views_ui import home, login_view, logout_view, register_view, dashboard_view

app_name = "core"

urlpatterns = [
    # Home page
    path('', home, name='home'),
    
    # Django session-based authentication
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('dashboard/', dashboard_view, name='dashboard'),
]