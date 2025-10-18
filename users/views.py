from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect


from users.forms import UserLoginForm, UserCreationForm


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Вы успешно вошли в систему.')
                return redirect('blog:index')
            else:
                messages.error(request, 'Неверный email или пароль.')
    else:
        form = UserLoginForm()

    context = {
        'title': 'Вход в аккаунт',
        'form': form
    }
    return render(request, 'users/login.html', context=context)


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('users/profile')  # Замените 'home' на имя вашего маршрута после успешной регистрации
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def logout_view(request):
    logout(request)
    context = {
        'title': 'Выход из аккаунта'
    }
    return render(request, 'users/logout.html', context=context)


def profile_view(request):
    user_object = request.user
    user_name = user_object.get_full_name() or user_object  # Если имя не заполнено, используем объект пользователя
    context = {
        'title': f'Ваш профиль {user_name}'
    }
    return render(request, 'users/profile.html', context=context)
