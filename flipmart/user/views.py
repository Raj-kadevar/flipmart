from math import perm

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from rest_framework import status
from user.models import Category
from user.forms import Registration, ProductForm, CategoryForm
from django.urls import reverse_lazy
from user.models import Product


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
            user = user.save()
            user.groups.add(Group.objects.get(name=request.POST['roles']))
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
            messages.success(request, 'product added successfully.')
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
            messages.success(request, 'category added successfully.')
            return redirect('add_category')
        else:
            errors = category.errors
            return render(request, "product_form.html", {"errors": errors, "form": category}, status=status.HTTP_400_BAD_REQUEST)

class UpdateCategory(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('user.change_category',)
    form_class = CategoryForm
    template_name = "category_form.html"
    success_url = reverse_lazy("index")
    queryset = Category.objects.all()




class DeleteCategory(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('user.delete_category',)
    model = Category
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("index")


class DeleteProduct(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('user.delete_product',)
    model = Product
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("index")


class UpdateProduct(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('user.change_product',)
    form_class = ProductForm
    template_name = "product_form.html"
    success_url = reverse_lazy("index")
    queryset = Category.objects.all()


class IndexView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        if request.user.has_perm("user.admin_access"):
            if request.user.has_perm("user.view_category"):
                categories = Category.objects.all()
                return render(request, "admin.html",{"categories":categories})
            return render(request, "admin.html")
        else:
            categories = Category.objects.all()
            return render(request,"index.html",{"categories":categories})


class ProductList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = ('user.view_product',)
    template_name = "admin_product.html"
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.filter(owner = self.request.user)


class ProductListView(LoginRequiredMixin, ListView):
    template_name = "product.html"
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.filter(type = self.kwargs['pk'])