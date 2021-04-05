from django.shortcuts import render, redirect

def index(request):
    return render(request, 'index.html')


def user_dash(request):
    return render(request, 'user_dash.html')


def driver_dash(request):
    return render(request, 'driver_dash.html')


def driver_chore(request):
    return render(request, 'driver_chore.html')

def user_chore(request):
    return render(request, 'user_chore.html')

def edit_user(request):
    return render(request, 'edit_user.html')
