from django.contrib import admin
from django.contrib.auth import get_user_model, admin as auth_admin
from user.models import Category, Product, Cart, OrderDetail, Address, Order

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    list_display = ["username"]

@admin.register(Category)
class Category(admin.ModelAdmin):
    list_display = ["id", "name"]

@admin.register(Product)
class Category(admin.ModelAdmin):
    list_display = ["id", "name", "price", "type", "stock"]

@admin.register(Cart)
class Cart(admin.ModelAdmin):
    list_display = ["id", "user", "product", "quantity"]

@admin.register(Order)
class Order(admin.ModelAdmin):
    list_display = ["id", "user", "address"]

@admin.register(OrderDetail)
class OrderDetail(admin.ModelAdmin):
    list_display = ["product", "price", "quantity", "order"]

@admin.register(Address)
class Address(admin.ModelAdmin):
    list_display = ["id", "street1", "street2", "address", "user"]
