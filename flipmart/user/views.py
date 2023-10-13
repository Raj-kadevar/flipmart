from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from rest_framework import status

from user.forms import Registration, ProductForm, CategoryForm, AddressForm
from user.models import Category, Cart, Address, OrderDetail as Order
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
            elif request.user.has_perm("user.view_product"):
                products = Product.objects.filter(owner = self.request.user)
                return render(request, "admin_product.html",{"products":products})
            return render(request, "admin.html")
        else:
            products = Product.objects.all()[0:4]
            categories = Category.objects.all()
            return render(request, "index.html", {"categories": categories, "products": products})


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
        product = Product.objects.get(id = kwargs['id'])
        category_id = product.type.id
        cart = Cart.objects.filter(product=product, user=request.user).first()
        if cart:
            quantity = cart.quantity
            cart.quantity = quantity+1
            messages.success(request, 'quantity +1 successfully.')
            cart.save()
        else:
            messages.success(request, 'product added successfully.')
            Cart.objects.get_or_create(user=request.user, product=product, quantity=1)
        if request.GET.get('result'):
            return redirect(reverse("order", kwargs = {'pk':kwargs.get('id')}))
        return redirect(reverse("category", kwargs = {'pk':category_id}))


class ManageQuantity(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        product = Product.objects.get(id = kwargs['id'])
        category_id = product.type.id
        cart = Cart.objects.filter(product=product, user=request.user).first()
        if cart:
            quantity = cart.quantity
            if quantity > 1 :
                messages.success(request, 'quantity -1 successfully.')
                cart.quantity = quantity-1
                cart.save()
            elif request.GET.get('result'):
                messages.success(request, 'minimum one product required')
                return redirect(reverse("order", kwargs={'pk': kwargs.get('id')}))
            else:
                cart.delete()
                messages.success(request, 'item removed successfully.')
            if request.GET.get('result'):
                return redirect(reverse("order", kwargs={'pk': kwargs.get('id')}))
        return redirect(reverse("category", kwargs = {'pk':category_id}))


class CartList(LoginRequiredMixin, ListView):
    template_name = "cart.html"
    context_object_name = "carts"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_carts'] = (Cart.objects.filter(user=self.request.user).values_list('product__id', flat=True))
        return context
    def get_queryset(self):
        carts = Cart.objects.filter(user=self.request.user)
        return carts


class DeleteCart(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        Cart.objects.get(id=self.kwargs['id']).delete()
        return redirect(reverse('cart'))


class ListAllProducts(LoginRequiredMixin, ListView):
    template_name = "all_products.html"
    queryset = Product.objects.all()
    context_object_name = "products"


class OrderDetail(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        address = Address.objects.filter(user=request.user)
        is_single_product = True
        if address:
            if kwargs.get('pk'):
                product_details = Product.objects.filter(id=kwargs.get('pk')).first()
                Cart.objects.get_or_create(user=request.user, product=product_details)
                return render(request, "confirm_order.html",
                              {"product": product_details, "is_single_product": is_single_product})
            else:
                product_details = Cart.objects.filter(user=request.user).values('product__id', 'product__name', 'product__price',
                                                                'product__image', 'quantity')
                return render(request, "confirm_order.html", {"products": product_details, "is_single_product": False})
        else:
            return redirect(reverse("set_address"))

    def post(self, request, *args, **kwargs):
        if kwargs.get('pk'):
            product = Product.objects.get(id=kwargs.get('pk'))
            Order.objects.create(user=request.user, product=product, quantity=1, price=product.price,
                                 address=request.user.address_set.first())
            messages.success(request, 'order placed successfully')
            return redirect("index")
        else:
            carts = Cart.objects.filter(user=request.user)
            Order.objects.create(user=request.user, address=request.user.address_set.first())

            for cart in carts:
                messages.success(request, 'orders placed successfully')
            Cart.objects.filter(user=request.user).delete()
            return redirect("index")


class SetAddress(CreateView):
    form_class = AddressForm
    template_name = "address.html"

    def post(self, request, *args, **kwargs):
        address = AddressForm(request.POST)
        if address.is_valid():
            address = address.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, 'address set successfully')
            return redirect('order')
        else:
            errors = address.errors
            return render(request, "form.html", {"errors": errors, "form": address}, status=status.HTTP_400_BAD_REQUEST)
