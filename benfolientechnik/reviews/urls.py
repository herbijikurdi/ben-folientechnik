from django.urls import path
from . import views

urlpatterns = [
    path('bewertungen/', views.reviews_page, name='reviews_page'),
]