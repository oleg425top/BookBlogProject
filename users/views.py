from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect


from users.forms import UserLoginForm


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


def register(request):
    pass


def logout(request):
    pass


def profile(request):
    pass
