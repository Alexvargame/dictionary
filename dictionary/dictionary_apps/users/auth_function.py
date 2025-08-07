from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Создаем пользователя
            message.success(request, 'URA')
            login(request, user)  # Залогиним пользователя сразу

            return redirect('main_page')  # Перенаправляем на главную страницу
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/user_registration.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        # Передаем данные формы корректно
        print(request.POST)
        form = CustomAuthenticationForm(data=request.POST)  # Передаем данные через 'data'
        if form.is_valid(): # Проверка на валидность формы
            print('EEYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY')
            user = form.cleaned_data['user']  # Получаем пользователя из формы
            login(request, user)  # Авторизуем пользователя
            messages.success(request, 'Вы успешно вошли в систему!')
            return redirect('api:main_page')  # Перенаправляем на главную страницу
        else:
            print('ERRRORROEROOEEERE', form.errors)
            messages.error(request, 'Неверный логин или пароль.')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'users/user_login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы.')
    return render(request, 'main_page.html')