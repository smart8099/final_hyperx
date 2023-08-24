from . import views
from django.urls import path

urlpatterns = [
    path("register", views.RegistrationAPIView.as_view(), name="register"),


]
