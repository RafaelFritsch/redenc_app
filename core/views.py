from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as app_login, logout as app_logout
from django.contrib import messages
from matriculas.views import *

# Create your views here.


def login(request):
    return render(request, 'login.html')

def submit_login(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            app_login(request, user)
            return redirect('user_rank')
        else:
            messages.error(request, 'Usuário ou senha inválidos')
    return redirect('login')

def logout(request):
    app_logout(request)
    return redirect('login')

