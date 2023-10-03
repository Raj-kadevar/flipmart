from django.urls import path

from user.views import IndexView, RegistrationView, UserLoginView

urlpatterns = [
    path("", IndexView, name="index"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("registration/", RegistrationView.as_view(), name="registration"),
]
