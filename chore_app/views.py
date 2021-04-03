from django.shortcuts import render, redirect

def index(request):
    return render(request, 'index.html')


def user_dash(request):
    return render(request, 'user_dash.html')
