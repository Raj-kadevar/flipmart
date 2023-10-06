from django.urls import path
from user.views import RegistrationView, UserLoginView, IndexView, AddProduct, AddCategory

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("registration/", RegistrationView.as_view(), name="registration"),
    path("add-product/", AddProduct.as_view(), name="add_product"),
    path("add-category/", AddCategory.as_view(), name="add_category"),
    path("product/<int:id>", AddCategory.as_view(), name="product"),
]
