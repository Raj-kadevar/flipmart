from math import perm

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from rest_framework import status
from user.models import Category, Cart
from user.forms import Registration, ProductForm, CategoryForm
from django.urls import reverse_lazy, reverse
from user.models import Product


class  UserLoginView(LoginView):
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
            messages.success(request, 'registration successful.')
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

class AddCategory(PermissionRequiredMixin, CreateView):
    form_class = CategoryForm
    template_name = "category_form.html"
    permission_required = ('user.add_category',)
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
            elif request.user.has_perm("user.view_category"):
                products = Product.objects.filter(owner = self.request.user)
                return render(request, "admin_product.html",{"products":products})
            return render(request, "admin.html")
        else:
            categories = Category.objects.all()
            return render(request,"index.html",{"categories":categories})


class AdminProductList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = ('user.view_product',)
    template_name = "admin_product.html"
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.filter(owner = self.request.user)


class ProductList(LoginRequiredMixin, ListView):
    template_name = "product.html"
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['carts'] = (Cart.objects.filter(user=self.request.user).values_list('product__id', flat=True))
        return context
    def get_queryset(self):
        products = Product.objects.filter(type = self.kwargs['pk'])
        return products


class AddToCart(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        messages.success(request, 'product added successfully.')
        product = Product.objects.get(id = kwargs['id'])
        category_id = product.type.id
        cart = Cart.objects.filter(product=product, user=request.user).first()
        if cart:
            quantity = cart.quantity
            cart.quantity = quantity+1
            cart.save()
        else:
            Cart.objects.create(user=request.user, product=product, quantity=1)
        return redirect(reverse("category", kwargs = {'pk':category_id}))


class ManageQuantity(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        product = Product.objects.get(id = kwargs['id'])
        category_id = product.type.id
        cart = Cart.objects.filter(product=product, user=request.user).first()
        if cart:
            quantity = cart.quantity
            if quantity > 1 :
                cart.quantity = quantity-1
                cart.save()
                messages.success(request, 'product remove successfully.')
            else:
                cart.delete()
                messages.success(request, 'item removed successfully.')

        return redirect(reverse("category", kwargs = {'pk':category_id}))


class CartList(LoginRequiredMixin, ListView):
    template_name = "cart.html"
    context_object_name = "carts"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_carts'] = (Cart.objects.filter(user=self.request.user).values_list('product__id', flat=True))
        return context
    def get_queryset(self):
        carts = Cart.objects.all()
        return carts

