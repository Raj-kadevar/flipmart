from django.contrib.auth.forms import UserCreationForm, get_user_model
from django import forms
from django.contrib.auth.models import Group

from user.models import Product, Category, Address

User = get_user_model()


class Registration(UserCreationForm):
    groups = [(name, name) for name in Group.objects.all().values_list('name', flat=True)]
    roles = forms.ChoiceField(choices= groups)
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'roles']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'image', 'price', 'about', 'type', 'stock']

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price < 50:
            raise forms.ValidationError("price should be more then 50.")
        return price

    def clean_image(self):

        image = self.cleaned_data.get('image')
        if not image:
            raise forms.ValidationError("image cannot be empty.")
        elif image and image.size > 5 * 1024 * 1024:
            raise forms.ValidationError("image size should be less than 5MB.")
        return image

    def clean_about(self):
        about = self.cleaned_data.get('about')
        if not about:
            raise forms.ValidationError("about require.")
        return about

    def clean_type(self):
        type = self.cleaned_data.get('type')
        if not type:
            raise forms.ValidationError("type require.")
        return type

    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock < 1:
            raise forms.ValidationError("stock should be more then 0")
        return stock



class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'image', 'description']

    def clean_image(self):

        image = self.cleaned_data.get('image')
        if not image:
            raise forms.ValidationError("image cannot be empty.")
        elif image and image.size > 5 * 1024 * 1024:
            raise forms.ValidationError("image size should be less than 5MB.")
        return image

    def clean_about(self):
        description = self.cleaned_data.get('description')
        if not description:
            raise forms.ValidationError("description require.")
        return description


class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = ['street1', 'street2', 'address']
