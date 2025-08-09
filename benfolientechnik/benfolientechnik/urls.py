"""
URL configuration for benfolientechnik project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from home import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('impressum/', views.impressum, name='impressum'),
    path('galerie/', views.galerie, name='galerie'),
    path('bewertungen/', views.bewertungen, name='bewertungen'),
    path('kontakt/', views.kontakt, name='kontakt'),
    path('ueber-uns/', views.ueberuns, name='ueber-uns'),
    path('scheibentoenung/', views.scheibentoenung, name='scheibentoenung'),
    path('datenschutz/', views.datenschutz, name='datenschutz'),
    path('quellen/', views.quellen, name='quellen'),
    path('danke/', views.bewertungerfolgreich, name='bewertungerfolgreich'),
    path('erfolgreich/', views.kontakterfolgreich, name='kontakterfolgreich'),
]
