from urllib import request

from django.shortcuts import render, redirect
from account.models import UserProfile
from django.contrib import auth

def account(request):
    if request.method == "POST":
        username =request.POST.get("username")
        password = request.POST.get("password")

        user =auth.authenticate(request,username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect("home")
        else:
            return redirect("login")


    return render(request, "account/login.html")  

# ==============================login view==============================
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user =auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request,user)
            return redirect("home")
        else:
            return redirect("login")
        
    return render(request, "account/login.html")

# ==============================register view==============================

def register(request): 
    if request.method == "POST":
            name=request.POST.get("name")
            email=request.POST.get("email")
            password=request.POST.get("password")
            confirm_password=request.POST.get("confirm_password")

            if password != confirm_password:
                return render(request, "account/register.html", {"error": "Passwords do not match."})
                
            else:
                UserProfile = UserProfile(
                name=name,
                email=email,
                )

                UserProfile.set_password(password)

                UserProfile.save()
            return redirect("home")

    return render(request, "account/register.html") 