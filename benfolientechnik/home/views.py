from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def impressum(request):
    return render(request, 'impressum.html')

def galerie(request):
    return render(request, 'galerie.html')

def bewertungen(request):
    return render(request, 'bewertungen.html')

def kontakt(request):
    return render(request, 'kontakt.html')

def ueberuns(request):
    return render(request, 'ueber-uns.html')

def scheibentoenung(request):
    return render(request, 'scheibentoenung.html')

def datenschutz(request):
    return render(request, 'datenschutz.html')

def quellen(request):
    return render(request, 'quellen.html')