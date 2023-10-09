from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from rest_framework import status
from user.models import Category
from user.forms import Registration, ProductForm, CategoryForm
from django.urls import reverse_lazy

from flipmart.user.models import Product


class UserLoginView(LoginView):
    template_name = "login.html"


    def form_valid(self, form):
        messages.success(self.request, 'Login successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        super().form_invalid(form)
        return render(self.request, "login.html", {'error': 'username or password invalid','form':form},
                      status=status.HTTP_400_BAD_REQUEST)


class RegistrationView(CreateView):
    form_class = Registration
    template_name = "form.html"

    def post(self, request, *args, **kwargs):

        user = Registration(request.POST)
        if user.is_valid():
            user.save()
            messages.success(request, 'form submitted successfully.')
            return redirect('login')
        else:
            errors = user.errors
            return render(request, "form.html", {"errors": errors, "form": user}, status=status.HTTP_400_BAD_REQUEST)


class AddProduct(CreateView):
    form_class = ProductForm
    template_name = "product_form.html"

    def post(self, request, *args, **kwargs):
        product = ProductForm(request.POST, request.FILES)
        if product.is_valid():
            product_data = product.save()
            product_data.owner = request.user
            product_data.save()
            return redirect('add_product')
        else:
            errors = product.errors
            return render(request, "product_form.html", {"errors": errors, "form": product}, status=status.HTTP_400_BAD_REQUEST)

class AddCategory(CreateView):
    form_class = CategoryForm
    template_name = "category_form.html"

    def post(self, request, *args, **kwargs):
        category = CategoryForm(request.POST, request.FILES)
        if category.is_valid():
            category.save()
            return redirect('add_category')
        else:
            errors = category.errors
            return render(request, "product_form.html", {"errors": errors, "form": category}, status=status.HTTP_400_BAD_REQUEST)

class UpdateCategory(LoginRequiredMixin, UpdateView):

    form_class = CategoryForm
    template_name = "category_form.html"
    success_url = reverse_lazy("index")
    queryset = Category.objects.all()


class DeleteCategory(DeleteView):
    model = Category
    template_name = "conform_delete.html"
    success_url = "index"


class DeleteProduct(DeleteView):
    model = Product
    template_name = "conform_delete.html"
    success_url = "index"


class UpdateProduct(LoginRequiredMixin, UpdateView):

    form_class = ProductForm
    template_name = "product_form.html"
    success_url = reverse_lazy("index")
    queryset = Category.objects.all()


class IndexView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        if request.user.has_perm('user.admin_access'):
            categories = Category.objects.all()
            return render(request, "admin.html",{"categories":categories})
        else:
            categories = Category.objects.all()
            return render(request,"index.html",{"categories":categories})
