from django.contrib.auth.forms import UserCreationForm, get_user_model
from django import forms

from user.models import Product, Category

User = get_user_model()


class Registration(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'image', 'price', 'about', 'type']

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price < 50:
            raise forms.ValidationError("price should be more then 50.")
        return price

    def clean_name(self):
        name = self.cleaned_data.get('name')

        if not name:
            raise forms.ValidationError("Name cannot be empty.")
        return name

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


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'image', 'description']

    def clean_name(self):
        name = self.cleaned_data.get('name')

        if not name:
            raise forms.ValidationError("Name cannot be empty.")
        return name

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
