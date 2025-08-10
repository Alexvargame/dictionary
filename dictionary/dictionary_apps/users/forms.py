from django import forms
from django.contrib.auth import authenticate

from .models import BaseUser

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        model = BaseUser
        fields = ('email', 'username')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])  # Устанавливаем хэшированный пароль
        if commit:
            user.save()
        return user



class CustomAuthenticationForm(forms.Form):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={
        'class': 'border p-2 rounded text-black'
    }))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
        'class': 'border p-2 rounded text-black'
    }))



    def clean(self):
        cleaned_data = super().clean()  # Очистка данных
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        # Если оба поля заполнены, пытаемся аутентифицировать пользователя
        if email and password:
            user = authenticate(email=email, password=password)
            if user is None:
                raise forms.ValidationError("Неверный логин или пароль")
            cleaned_data['user'] = user  # Сохраняем пользователя в данных
        return cleaned_data