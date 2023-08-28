from . import views
from django.urls import path

urlpatterns = [
    path("register", views.RegistrationAPIView.as_view(), name="register"),
    path("login", views.LoginAPIView.as_view(), name="login"),
    path("refresh-token", views.CustomTokenRefreshView.as_view(), name="refresh_token"),
    path('change-password/', views.PasswordChangeView.as_view(), name='change-password'),



]
