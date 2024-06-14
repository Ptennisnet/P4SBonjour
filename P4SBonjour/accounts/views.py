from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from .models import MFA
from .forms import MFAForm
from datetime import datetime, timezone, timedelta


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            # Return an 'invalid login' error message.
            return render(request, 'login_incorrect.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')


def login_incorrect_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            # Return an 'invalid login' error message.
            return render(request, 'login_incorrect.html', {'error': 'Invalid username or password'})
    return render(request, 'login_incorrect.html')


def login_lockout_view(request):
    return render(request, 'login_lockout.html')


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def send_mfa_code(request):
    code = get_random_string(length=6, allowed_chars='0123456789')
    expiration_time = datetime.now(timezone.utc) + timedelta(minutes=10)
    MFA.objects.create(user=request.user, code=code, expires_at=expiration_time)

    send_mail(
        'Your MFA Code',
        f'Your MFA code is {code}',
        'bonjouremailserver@gmail.com',
        [request.user.email],
        fail_silently=False,
    )

    return render(request, 'send_mfa_code.html')


@login_required
def verify_mfa(request):
    if request.method == 'POST':
        form = MFAForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            mfa = MFA.objects.filter(user=request.user, code=code).first()
            if mfa and mfa.is_valid():
                # Mark user as verified
                request.session['mfa_verified'] = True
                return redirect('home')
            else:
                form.add_error('code', 'Invalid or expired code')
    else:
        form = MFAForm()

    return render(request, 'verify_mfa.html', {'form': form})
