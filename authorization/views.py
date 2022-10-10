from textwrap import dedent

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.template.defaulttags import register
from store.models import Customer
from django.db.models import Q

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


def register(request):
    if request.method == 'POST':
        errors = dict()
        if User.objects.filter(email=request.POST['email']).exists():
            errors['email'] = 'Данный e-mail уже используется.'
        if User.objects.filter(username=request.POST['username']).exists():
            errors['username'] = 'Данный никнейм уже используется.'
        if request.POST['password'] != request.POST['password_confirm']:
            errors['password_confirm'] = 'Пароли не совпадают'
        try:
            validate_password(request.POST['password'])
        except ValidationError:
            errors['password'] = dedent(
                '''
                Некорректный пароль.
                Пароль должен быть:
                   длиной не менее 8-ми символов;
                   состоять из цифр и букв (как минимум одна заглавная);
                   быть сложным (не использовать qwerty и тому подобные комбинации).'''
            )
        if errors:
            return render(request, 'sign_up.html', {'errors': errors, 'entered_data': request.POST})

        user = User.objects.create(
            username=request.POST['username'],
            email=request.POST['email'],
            first_name=request.POST['first_name'],
            password=request.POST['password']
        )
        customer = Customer.objects.create(
            user=user
        )
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('my_rent')

    return render(request, 'sign_up.html')


def password_reset(request):
    if request.method == 'POST':
        try:
            user = User.objects.get(
                Q(email=request.POST["email_or_username"]) | \
                Q(username=request.POST["email_or_username"])
            )
        except User.DoesNotExist:
            return render(request, 'password_reset.html', {'errors': {'email_or_username': 'Пользователь не найден'}})
        
    return render(request, 'password_reset.html')


@login_required(login_url='sign_in')
def change_password(request):
    errors = dict()
    if request.method == 'POST':
        
        print(request.user)
        user = request.user
        if user.check_password(request.POST['old_password']):
            if request.POST['new_password'] != request.POST['new_password_confirm']:
                errors['password_confirm'] = 'Пароли не совпадают'
            try:
                validate_password(request.POST['new_password'])
            except ValidationError:
                errors['password'] = dedent(
                    '''
                    Некорректный пароль.
                    Пароль должен быть:
                    длиной не менее 8-ми символов;
                    состоять из цифр и букв (как минимум одна заглавная);
                    быть сложным (не использовать qwerty и тому подобные комбинации).'''
                )
            if not errors:
                user.set_password(request.POST['new_password'])
                user.save()
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('my_rent')
        else:
            errors['incorrect_password'] = 'Неправильный пароль'
    return render(request, 'change_password.html', {'errors': errors})
