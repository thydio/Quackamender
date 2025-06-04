from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password

# Create your views here.
def login(r):
    if r.method == "POST":
        username = r.POST.get('username')
        password = r.POST.get('password')
        user = authenticate(r, username=username, password=password)
        if user is not None:
            auth_login(r, user)
            return redirect('home')  # Replace 'home' with your desired redirect URL name
        else:
            return render(r, 'login.html', {'error': 'Invalid credentials'})
    return render(r, 'login.html')



def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        if password != confirm_password:
            return render(request, "signup.html", {"error": "Passwords do not match"})
        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {"error": "Username already exists"})
        user = User.objects.create(username=username, password=make_password(password))
        user.save()
        return HttpResponseRedirect(reverse("login"))
    return render(request, "signup.html")