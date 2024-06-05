# mfa.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.http import HttpResponse

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            # User authentication succeeded, generate and send OTP via email
            otp = generate_otp()
            send_otp_email(user.email, otp)
            request.session['otp'] = otp
            return render(request, 'mfa/verify_otp.html')
        else:
            # User authentication failed
            return HttpResponse('Invalid username or password')
    else:
        return render(request, 'login.html')

def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        expected_otp = request.session.get('otp')
        if entered_otp == expected_otp:
            # OTP verification succeeded
            del request.session['otp']
            return HttpResponse('OTP verification successful')
        else:
            # OTP verification failed
            return HttpResponse('Invalid OTP')
    else:
        return render(request, 'mfa/verify_otp.html')

def generate_otp():
    # Generate a random 6-digit OTP (you may use your own OTP generation logic)
    import random
    return str(random.randint(100000, 999999))

def send_otp_email(email, otp):
    subject = 'Your OTP for MFA'
    message = f'Your OTP for Multi-Factor Authentication is: {otp}'
    from_email = 'your_email@example.com'  # Replace with your email address
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)
