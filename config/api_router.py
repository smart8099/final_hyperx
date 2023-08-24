from django.urls import include, path

urlpatterns = [
    path("auth/", include("hyperx.accounts.urls"), name="auth"),
]
