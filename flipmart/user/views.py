from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.views.generic import CreateView
from rest_framework import status

from user.forms import Registration


class IndexView:
    pass


class UserLoginView(LoginView):
    template_name = "login.html"

    def form_invalid(self, form):
        return render(self.request, "login.html", {'error': 'username or password invalid','form':form},
                      status=status.HTTP_400_BAD_REQUEST)


class RegistrationView(CreateView):
    form_class = Registration
    template_name = "form.html"

    def post(self, request, *args, **kwargs):

        user = Registration(request.POST)
        if user.is_valid():
            user.save()
            return redirect('login')
        else:
            errors = user.errors
            return render(request, "form.html", {"errors": errors, "form": user}, status=status.HTTP_400_BAD_REQUEST)
