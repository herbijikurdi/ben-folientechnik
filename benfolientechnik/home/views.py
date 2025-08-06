from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def impressum(request):
    return render(request, 'impressum.html')