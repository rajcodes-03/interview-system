from django.shortcuts import render

def account(request):
    return render(request, "account/login.html")  

def register(request):
    return render(request, "account/register.html")