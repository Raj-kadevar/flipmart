from django.urls import path
from django.views.generic import TemplateView
from user.views import RegistrationView, UserLoginView

urlpatterns = [
    path("", TemplateView.as_view(template_name = 'index.html'), name="index"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("registration/", RegistrationView.as_view(), name="registration"),
]
