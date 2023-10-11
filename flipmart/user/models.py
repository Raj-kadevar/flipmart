from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import ImageField


class User(AbstractUser):
    profile = ImageField(blank=True, null=True, upload_to="profile/")


class Category(models.Model):
    name = models.CharField(blank=False, max_length=20)
    image = models.ImageField(upload_to="Categories/")
    description = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(blank=False, max_length=30)
    image = models.ImageField(upload_to="products/")
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    about = models.CharField(max_length=200, blank=True)
    type = models.ForeignKey(Category, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(blank=False, null=False)


class Address(models.Model):
    street1 = models.CharField(blank=True, null=False, max_length=50)
    street2 = models.CharField(blank=True, null=True, max_length=50)
    address = models.CharField(blank=True, null=True, max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class OrderDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(blank=False, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)

class CustomPermissions(models.Model):

    class Meta:
        managed = False
        default_permissions = ()

        permissions = (('admin_access', 'can use admin panel'),)