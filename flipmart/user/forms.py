from django.contrib.auth.forms import UserCreationForm, get_user_model
User = get_user_model()


class Registration(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
