from django.contrib.auth.views import LogoutView
from django.urls import path
from user.views import RegistrationView, UserLoginView, IndexView, AddProduct, AddCategory, \
    ProductList, AdminProductList, AddToCart, ManageQuantity, CartList, DeleteCart, ListAllProducts, OrderDetail, \
    SetAddress
from user.views import UpdateCategory, UpdateProduct, DeleteCategory, DeleteProduct

urlpatterns = [
    path("", IndexView.as_view(), name="index"),

    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),

    path("registration/", RegistrationView.as_view(), name="registration"),

    path("add-category/", AddCategory.as_view(), name="add_category"),
    path("update-category/<int:pk>", UpdateCategory.as_view(), name="update_category"),
    path("delete-category/<int:pk>", DeleteCategory.as_view(), name="delete_category"),

    path("add-product/", AddProduct.as_view(), name="add_product"),
    path("product/<int:pk>", UpdateProduct.as_view(), name="update_product"),
    path("delete-product/<int:pk>", DeleteProduct.as_view(), name="delete_product"),

    path("product-list", AdminProductList.as_view(), name="product_list"),
    path("product-list/<int:pk>", ProductList.as_view(), name="category"),

    path("add-to-cart/<int:id>", AddToCart.as_view(), name="add_to_cart"),
    path("manage-quantity/<int:id>", ManageQuantity.as_view(), name="manage_quantity"),
    path("my-cart/", CartList.as_view(), name="cart"),
    path("remove-cart/<int:id>", DeleteCart.as_view(), name="remove_cart"),

    path("all-products/", ListAllProducts.as_view(), name="all_products"),
    path("order/<int:pk>", OrderDetail.as_view(), name="order"),
    path("order/", OrderDetail.as_view(), name="order"),
    path("set-address/", SetAddress.as_view(), name="set_address"),
]
