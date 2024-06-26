from django.contrib import messages, auth
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage

from .forms import RegistrationForm
from .models import Account

import requests

# Create your views here.


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        # user valid
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            # confirm_password = form.cleaned_data['confirm_password']

            user = Account.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email,
            )
            user.phone_number = phone_number
            user.save()

            # user activision
            curent_site = get_current_site(request)
            mail_subject = 'لطفا اکانتتان را فعال کنید .'
            message = render_to_string(
                'accounts/account_verification_email.html', {
                    'user': user,
                    'domain': curent_site,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            return redirect(
                '/accounts/login/?command-verification&email='+email)
        else:
            # Form is not valid
            return render(request, 'accounts/register.html', {'form': form})
    else:
        form = RegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            # messages.success(request , 'شما وارد شدید .')
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except ValueError:
                return redirect('dashboard:profile_page')

        else:
            messages.error(request, 'رمز عبور خود را بازنشانی کنید .')
            return redirect('account:login_page')

    return render(request, 'accounts/login.html')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'تبریک ! حساب شما با موفقیت تایید شد .')
        return redirect('account:login_page')
    else:
        messages.error(request, 'لینک فعالسازی نامعتبر است .')
        return redirect('account:register_page')


@login_required(login_url='account:login_page')
def logout(request):
    auth.logout(request)
    messages.success(request, 'شما خارج شدید .')
    return redirect('account:login_page')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        # check the email for existing in db (exact email or not)
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email=email)

            # reset password email
            curent_site = get_current_site(request)
            mail_subject = 'لطفا اکانتتونو تایید کنید برای تغییر رمز عبورتان.'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': curent_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(
                request, 'بازنشانی رمز عبور به ادرس ایمیلتان ارسال شد .')
            return redirect('account:login_page')
        else:
            messages.error(request, 'اکانت مورد نظر وجود ندارد .')
            return redirect('account:forgot_password_page')
    return render(request, 'accounts/forgot_password_checks.html')


def reset_password_validate(request, uidb64, token):
    try:
        # تبدیل uidb64 به شناسه کاربری و یافتن کاربر
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        # اگر توکن معتبر است، اقدامات بعدی را انجام دهید
        request.session['uid'] = uid
        messages.success(request, 'لطفا رمز عبور خودتان را بازنشانی کنید .')
        return redirect('account:reset_password_page')
    else:
        # اگر توکن منقضی یا نامعتبر است
        messages.error(request, 'این لینک منقضی شده است .')
        return redirect('account:login_page')


def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'با موفقیت رمز عبور باز نشانی شد .')
            return redirect('account:login_page')
        else:
            messages.error(request, 'رمز عبور مطابقت ندارد .')
            return redirect('account:reset_password_page')
    else:
        return render(request, 'accounts/password-update.html')
#-------------
# from django.shortcuts import render, HttpResponse, redirect
# from .forms import ShopUserCreationForm, LoginForm
# from django.contrib.auth import authenticate, login, logout


# # Create your views here.

# def register(request):
#     if request.method == 'POST':
#         form = ShopUserCreationForm(request.POST)
#         # user valid
#         if form.is_valid():
#             user = form.save()
#             return HttpResponse('user created')
#     else:
#         form = ShopUserCreationForm()
#     return render(request, 'shop/register.html', {'form': form})


# def user_login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             form = form.cleaned_data
#             phone = form['phone']
#             password = form['password']
#             user = authenticate(phone=phone, password=password)
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return HttpResponse('you entered')
#                 else:
#                     return HttpResponse('you are not active!')
#             else:
#                 return HttpResponse('you are not registered!')
#     else:
#         form = LoginForm()
#     return render(request, 'shop/login.html', {'form': form})


# def user_logout(request):
#     logout(request)
#     return redirect(request.META.get('HTTP_REFERER'))
