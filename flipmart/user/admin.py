from django.contrib import admin
from django.contrib.auth import get_user_model, admin as auth_admin
from user.models import Category, Product

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    list_display = ["username"]

@admin.register(Category)
class Category(admin.ModelAdmin):
    list_display = ["id", "name"]

@admin.register(Product)
class Category(admin.ModelAdmin):
    list_display = ["id", "name", "price", "type"]
