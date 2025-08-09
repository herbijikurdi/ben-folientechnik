from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('impressum/', views.impressum, name='impressum'),
    path('galerie/', views.galerie, name='galerie'),
    path('bewertungen/', views.bewertungen, name='bewertungen'),
    path('kontakt/', views.kontakt, name='kontakt'),
    path('ueber-uns/', views.ueberuns, name='ueber-uns'),
    path('schreibentoenung/', views.scheibentoenung, name='scheibentoenung'),
    path('datenschutz/', views.datenschutz, name='datenschutz'),
    path('quellen/', views.quellen, name='quellen'),
    path('danke/', views.bewertungerfolgreich, name="bewertungerfolgreich"),
    path('erfolgreich/', views.kontakterfolgreich, name="kontakterfolgreich"),
]