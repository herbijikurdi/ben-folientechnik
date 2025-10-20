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
from django.conf import settings
from django.conf.urls.static import static
from home import views

urlpatterns = [
    # Django Admin auf neuen Pfad verschieben
    path('django-admin/', admin.site.urls),
    
    # Eigenes Admin Dashboard
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    
    # Admin AJAX APIs
    path('admin/reviews/<int:review_id>/status/', views.admin_review_action, name='admin_review_action'),
    path('admin/reviews/<int:review_id>/delete/', views.admin_review_delete, name='admin_review_delete'),
    
    # Galerie Admin AJAX APIs
    path('admin/gallery/add/', views.admin_gallery_add, name='admin_gallery_add'),
    path('admin/gallery/<int:gallery_id>/data/', views.admin_gallery_data, name='admin_gallery_data'),
    path('admin/gallery/<int:gallery_id>/edit/', views.admin_gallery_edit, name='admin_gallery_edit'),
    path('admin/gallery/<int:gallery_id>/delete/', views.admin_gallery_delete, name='admin_gallery_delete'),
    path('admin/gallery/<int:gallery_id>/toggle/', views.admin_gallery_toggle_active, name='admin_gallery_toggle_active'),
    
    # Normale Website URLs
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

# Media files serving in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
