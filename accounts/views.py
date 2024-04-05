from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to a home page
        else:
            messages.error(request, 'Username or Password is incorrect')
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    # Redirect to homepage or any other page
    return redirect('/')

