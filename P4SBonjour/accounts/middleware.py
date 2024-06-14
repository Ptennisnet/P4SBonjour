import mailbox
import time
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.cache import cache
from django.conf import settings
import accesscontrol


class LoginDelayMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.last_login_attempt_time = 0

    def __call__(self, request):
        if request.path == '/login/' and request.method == 'POST':
            current_time = time.time()
            time_since_last_attempt = current_time - self.last_login_attempt_time

            if time_since_last_attempt < 20:
                return HttpResponse('Please wait a few seconds before trying again.', status=429)

            self.last_login_attempt_time = current_time

        response = self.get_response(request)
        return response


class CriticalFunction:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if "superuser_password":
            cache_super = accesscontrol.get_super_user(1024)


class LoginLockoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST' and ((request.path == '/login/') or (request.path == '/login_incorrect/')):
            username = request.POST.get('username')
            if username:
                cache_key = f'login_attempts_{username}'
                login_attempts = cache.get(cache_key, {'count': 0, 'last_attempt_time': time.time()})

                if login_attempts['count'] >= settings.MAX_LOGIN_ATTEMPTS:
                    if time.time() - login_attempts['last_attempt_time'] < settings.LOGIN_TIMEOUT:
                        return redirect('login_lockout')  # redirect to a timeout page

                user = authenticate(request, username=username, password=request.POST.get('password'))
                if user is None:
                    login_attempts['count'] += 1
                    login_attempts['last_attempt_time'] = time.time()
                    cache.set(cache_key, login_attempts, timeout=settings.LOGIN_TIMEOUT)
                else:
                    cache.delete(cache_key)

        response = self.get_response(request)
        return response
