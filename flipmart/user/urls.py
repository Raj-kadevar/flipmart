from django.urls import path
from user.views import RegistrationView, UserLoginView, IndexView, AddProduct, AddCategory

from flipmart.user.views import UpdateCategory, UpdateProduct, DeleteCategory, DeleteProduct

urlpatterns = [
    path("", IndexView.as_view(), name="index"),

    path("login/", UserLoginView.as_view(), name="login"),
    path("registration/", RegistrationView.as_view(), name="registration"),

    path("add-category/", AddCategory.as_view(), name="add_category"),
    path("update-category/<int:id>", UpdateCategory.as_view(), name="update_category"),
    path("delete-category/<int:id>", DeleteCategory.as_view(), name="delete_category"),

    path("add-product/", AddProduct.as_view(), name="add_product"),
    path("product/<int:id>", UpdateProduct.as_view(), name="update_product"),
    path("delete-product/<int:id>", DeleteProduct.as_view(), name="delete_product"),


]
