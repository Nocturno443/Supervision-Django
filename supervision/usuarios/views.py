from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            messages.success(request, ("Te has Logueado.."))
            return render(request, 'product_list.html')
        else:
            messages.success(request, ("Hubo un error, por favor trate de nuevo.."))
            return render(request, 'login.html', {})   

    return render(request, "login.html", {"login":login}) 


def logout_user(request):
    logout(request)
    messages.success(request, ("Has salido de tu Usuario.."))
    return render(request, 'login.html', {})