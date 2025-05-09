from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import ausleihe_view
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='startseite'), name='logout'),
    path('register/', views.register, name='register'),
    path('ausleihe/', ausleihe_view, name='ausleihe'),
]