from django.shortcuts import render, redirect
from django.db import models
from reviews.models import Review, Gallery, GalleryImage
from django.db.models import Count, Avg
from django.core.mail import send_mail
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone
from datetime import timedelta
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os

def index(request):
    # Hole die besten/neuesten Bewertungen für die Startseite
    # Temporär: Alle Bewertungen anzeigen bis Status-Filter aktiv ist
    featured_reviews = Review.objects.filter(status='approved').order_by('-created_at')[:3]  # 3 neueste genehmigte Bewertungen
    
    # Durchschnittsbewertung berechnen (nur genehmigte Bewertungen)
    all_reviews = Review.objects.filter(status='approved')
    average_rating = all_reviews.aggregate(average=Avg('rating'))['average'] or 0
    average_rating = round(average_rating, 1)
    total_reviews = all_reviews.count()
    
    # Sterne-Anzeige: Ab 4.75 werden alle 5 Sterne angezeigt
    if average_rating >= 4.75:
        star_types = ['full'] * 5
    else:
        import math
        # Aufrundung auf halbe Sterne: 2.25→2.5, 2.75→3.0, 3.25→3.5, usw.
        rounded_rating = math.ceil(average_rating * 2) / 2
        full_stars = math.floor(rounded_rating)
        has_half_star = (rounded_rating - full_stars) > 0
        star_types = []
        for i in range(1, 6):
            if i <= full_stars:
                star_types.append('full')
            elif i == full_stars + 1 and has_half_star:
                star_types.append('half')
            else:
                star_types.append('empty')
    
    context = {
        'featured_reviews': featured_reviews,
        'average_rating': average_rating,
        'total_reviews': total_reviews,
        'star_types': star_types,
    }
    return render(request, 'index.html', context)

def impressum(request):
    return render(request, 'impressum.html')

def galerie(request):
    gallery_images = Gallery.objects.filter(is_active=True).order_by('order', '-created_at')
    context = {
        'gallery_images': gallery_images,
    }
    return render(request, 'galerie.html', context)

def bewertungen(request):
    return render(request, 'bewertungen.html', context={})

def kontakterfolgreich(request):
    return render(request, "kontakt_erfolgreich.html")

def kontakt(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        email = request.POST.get("email")
        telefon = request.POST.get("phone")
        firma = request.POST.get("company") if request.POST.get("company").strip() != "" else "Keine Firma angegeben"
        leistung = request.POST.get("service")
        nachricht = request.POST.get("message")

        send_mail(
            subject=f"Neue Anfrage von {name}",
            message=f"Von: {name}\nE-Mail: {email}\nFirma: {firma}\nTelefon: {telefon}\nLeistung: {leistung}\n\nNachricht:\n{nachricht}",
            from_email=email,
            recipient_list=['info@ben-folientechnik.de'],
            fail_silently=False,
        )
        return redirect('kontakterfolgreich')
    else:
        return render(request, "kontakt.html")

def ueberuns(request):
    return render(request, 'ueber-uns.html')

def scheibentoenung(request):
    return render(request, 'scheibentoenung.html')

def datenschutz(request):
    return render(request, 'datenschutz.html')

def quellen(request):
    return render(request, 'quellen.html')

def bewertungerfolgreich(request):
    return render(request, 'bewertung_erfolgreich.html')


def bewertungen(request):
    if request.method == "POST":
        name = request.POST.get("name")
        if not name.strip():
            name = "Anonym"
        email = request.POST.get("email", "")
        service = request.POST.get("service")
        if service.lower() == "scheibentonung":
            service = "Scheibentönung"
        elif service.lower() == "sonstiges":
            service = "Sonstiges"
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")

        # Temporär: Ohne status Feld bis Migration läuft
        Review.objects.create(
            name=name,
            email=email,
            service=service,
            rating=rating,
            comment=comment,
            status='pending'  # Nach Migration wieder aktivieren
        )
        return redirect('bewertungerfolgreich')

    # Temporär: Alle Bewertungen anzeigen bis Migration läuft
    # Nach Migration ändern zu: reviews = Review.objects.filter(status='approved').order_by('-created_at')
    reviews = Review.objects.filter(status='approved').order_by('-created_at')
    total_reviews = reviews.count()

    rating_counts = reviews.values('rating').annotate(count=Count('rating')).order_by('rating')
    rating_dict = {entry['rating']: entry['count'] for entry in rating_counts}
    average_rating = reviews.aggregate(average=Avg('rating'))['average'] or 0
    average_rating = round(average_rating, 1)
    average_rating_rounded = int(round(average_rating))

    rating_percentages = {}
    for i in range(1, 6):
        count = rating_dict.get(i, 0)
        percent = (count / total_reviews * 100) if total_reviews > 0 else 0
        rating_percentages[i] = round(percent)

    # Sterne-Anzeige für Durchschnittsbewertung
    if average_rating >= 4.75:
        star_types = ['full'] * 5
    else:
        import math
        # Aufrundung auf halbe Sterne: 2.25→2.5, 2.75→3.0, 3.25→3.5, usw.
        rounded_rating = math.ceil(average_rating * 2) / 2
        full_stars = math.floor(rounded_rating)
        has_half_star = (rounded_rating - full_stars) > 0
        star_types = []
        for i in range(1, 6):
            if i <= full_stars:
                star_types.append('full')
            elif i == full_stars + 1 and has_half_star:
                star_types.append('half')
            else:
                star_types.append('empty')

    # Sterne für jede einzelne Bewertung berechnen
    for review in reviews:
        if review.rating >= 4.75:
            review.star_types = ['full'] * 5
        else:
            import math
            rounded_rating = math.ceil(review.rating * 2) / 2
            full_stars = math.floor(rounded_rating)
            has_half_star = (rounded_rating - full_stars) > 0
            review.star_types = []
            for i in range(1, 6):
                if i <= full_stars:
                    review.star_types.append('full')
                elif i == full_stars + 1 and has_half_star:
                    review.star_types.append('half')
                else:
                    review.star_types.append('empty')

    context = {
        'reviews': reviews,
        'total_reviews': total_reviews,
        'rating_percentages': rating_percentages,
        'average_rating': average_rating,
        'average_rating_rounded': average_rating_rounded,
        'star_types': star_types,
    }
    return render(request, 'bewertungen.html', context)


# Admin Dashboard View
@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    """
    Admin Dashboard View - nur für Superuser zugänglich
    """
    # Statistiken berechnen
    total_reviews = Review.objects.count()
    
    # Bewertungen der letzten Woche
    week_ago = timezone.now() - timedelta(days=7)
    new_reviews = Review.objects.filter(created_at__gte=week_ago).count()
    
    # Durchschnittsbewertung aller genehmigten Bewertungen
    approved_reviews = Review.objects.filter(status='approved')
    average_rating = approved_reviews.aggregate(avg=Avg('rating'))['avg']
    average_rating = round(average_rating, 1) if average_rating else 0.0
    
    # Alle Bewertungen für die Tabelle
    reviews = Review.objects.order_by('-created_at')
    
    # Galerie-Bilder für die Galerie-Verwaltung
    gallery_images = Gallery.objects.order_by('order', '-created_at')
    
    # Temporär: Simuliere Status-Filter bis Migration läuft
    # Nach Migration diese Zeilen durch echte Filter ersetzen:
    # approved_reviews = reviews.filter(status='approved')
    # pending_reviews = reviews.filter(status='pending') 
    # rejected_reviews = reviews.filter(status='rejected')
    
    approved_reviews = reviews.filter(status='approved')
    pending_reviews = reviews.filter(status='pending')
    rejected_reviews = reviews.filter(status='rejected')
    
    # Simulierte Daten für andere Bereiche (später durch echte Modelle ersetzen)
    pending_contacts = 0  # Später durch Kontakt-Model ersetzen
    new_contacts = 0
    pending_appointments = 0  # Später durch Termin-Model ersetzen
    
    # Letzte Aktivitäten (simuliert)
    recent_activities = [
        {
            'description': f'Neue Bewertung von {reviews.first().name if reviews.exists() else "Unbekannt"}' if reviews.exists() else 'Keine Aktivitäten',
            'icon': 'star',
            'created_at': reviews.first().created_at if reviews.exists() else timezone.now()
        }
    ]
    
    context = {
        'total_reviews': total_reviews,
        'new_reviews': new_reviews,
        'pending_contacts': pending_contacts,
        'new_contacts': new_contacts,
        'pending_appointments': pending_appointments,
        'average_rating': average_rating,
        'reviews': reviews,
        'approved_reviews': approved_reviews,
        'pending_reviews': pending_reviews,
        'rejected_reviews': rejected_reviews,
        'gallery_images': gallery_images,
        'recent_activities': recent_activities,
    }
    
    return render(request, 'admin.html', context)


# AJAX API Views für Admin-Aktionen
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@user_passes_test(lambda u: u.is_superuser)
@csrf_exempt
def admin_review_action(request, review_id):
    """
    AJAX endpoint für Bewertungsaktionen (genehmigen/ablehnen)
    TEMPORÄR: Funktioniert erst nach Migration
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            action = data.get('status')
            
            review = Review.objects.get(id=review_id)
            
            if action in ['approved', 'rejected']:
                review.status = action
                review.save()
                
                return JsonResponse({
                    'success': True,
                    'message': f'Bewertung wurde {action}.',
                    'status': action
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Ungültige Aktion.'
                })
                
        except Review.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Bewertung nicht gefunden.'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            })
    
    return JsonResponse({'success': False, 'message': 'Nur POST erlaubt.'})


@user_passes_test(lambda u: u.is_superuser)
@csrf_exempt
def admin_review_delete(request, review_id):
    """
    AJAX endpoint zum Löschen von Bewertungen
    """
    if request.method == 'DELETE':
        try:
            review = Review.objects.get(id=review_id)
            review.delete()
            
            return JsonResponse({
                'success': True,
                'message': 'Bewertung wurde gelöscht.'
            })
            
        except Review.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Bewertung nicht gefunden.'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            })
    
    return JsonResponse({'success': False, 'message': 'Nur DELETE erlaubt.'})


# Galerie Admin Views
@user_passes_test(lambda u: u.is_superuser)
@csrf_exempt
def admin_gallery_add(request):
    """
    AJAX endpoint zum Hinzufügen eines Galerie-Eintrags mit mehreren Bildern
    """
    if request.method == 'POST':
        try:
            title = request.POST.get('title', '').strip()
            description = request.POST.get('description', '').strip()
            category = request.POST.get('category', '').strip()
            order = request.POST.get('order', 0)
            is_active = request.POST.get('is_active', 'true') == 'true'
            images = request.FILES.getlist('images')

            if not title:
                return JsonResponse({'success': False, 'message': 'Titel ist erforderlich.'})

            if not images:
                return JsonResponse({'success': False, 'message': 'Mindestens ein Bild ist erforderlich.'})

            # Galerie-Eintrag erstellen
            gallery_item = Gallery.objects.create(
                title=title,
                description=description,
                category=category if category else '',
                order=int(order) if order else 0,
                is_active=is_active
            )

            # Bilder hinzufügen
            gallery_images = []
            for i, image_file in enumerate(images):
                gallery_image = GalleryImage.objects.create(
                    gallery=gallery_item,
                    image=image_file,
                    order=i
                )
                gallery_images.append({
                    'id': gallery_image.id,
                    'image_url': gallery_image.image.url,
                    'order': gallery_image.order
                })

            return JsonResponse({
                'success': True,
                'message': f'Galerie-Eintrag mit {len(images)} Bild(ern) wurde erfolgreich hinzugefügt.',
                'gallery_item': {
                    'id': gallery_item.id,
                    'title': gallery_item.title,
                    'description': gallery_item.description,
                    'category': gallery_item.category,
                    'image_count': len(images),
                    'main_image_url': gallery_images[0]['image_url'] if gallery_images else None,
                    'images': gallery_images,
                    'order': gallery_item.order,
                    'is_active': gallery_item.is_active,
                    'created_at': gallery_item.created_at.strftime('%d.%m.%Y %H:%M')
                }
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Fehler beim Hinzufügen: {str(e)}'
            })

    return JsonResponse({'success': False, 'message': 'Nur POST erlaubt.'})


@user_passes_test(lambda u: u.is_superuser)
@csrf_exempt
def admin_gallery_edit(request, gallery_id):
    """
    AJAX endpoint zum Bearbeiten eines Galerie-Eintrags mit mehreren Bildern
    """
    if request.method == 'POST':
        try:
            gallery_item = Gallery.objects.get(id=gallery_id)

            title = request.POST.get('title', '').strip()
            description = request.POST.get('description', '').strip()
            category = request.POST.get('category', '').strip()
            order = request.POST.get('order', 0)
            is_active = request.POST.get('is_active', 'true') == 'true'
            new_images = request.FILES.getlist('new_images')

            # Bilder zum Löschen
            images_to_delete = request.POST.get('images_to_delete', '')
            if images_to_delete:
                delete_ids = [int(id.strip()) for id in images_to_delete.split(',') if id.strip()]
                for img_id in delete_ids:
                    try:
                        gallery_image = GalleryImage.objects.get(id=img_id, gallery=gallery_item)
                        default_storage.delete(gallery_image.image.path)
                        gallery_image.delete()
                    except GalleryImage.DoesNotExist:
                        pass

            if not title:
                return JsonResponse({'success': False, 'message': 'Titel ist erforderlich.'})

            # Galerie-Eintrag aktualisieren
            gallery_item.title = title
            gallery_item.description = description
            gallery_item.category = category if category else ''
            gallery_item.order = int(order) if order else 0
            gallery_item.is_active = is_active
            gallery_item.save()

            # Neue Bilder hinzufügen
            if new_images:
                max_order = gallery_item.images.aggregate(max_order=models.Max('order'))['max_order'] or 0
                for i, image_file in enumerate(new_images):
                    GalleryImage.objects.create(
                        gallery=gallery_item,
                        image=image_file,
                        order=max_order + i + 1
                    )

            # Alle Bilder für Response sammeln
            gallery_images = []
            for img in gallery_item.images.all():
                gallery_images.append({
                    'id': img.id,
                    'image_url': img.image.url,
                    'order': img.order
                })

            return JsonResponse({
                'success': True,
                'message': 'Galerie-Eintrag wurde erfolgreich aktualisiert.',
                'gallery_item': {
                    'id': gallery_item.id,
                    'title': gallery_item.title,
                    'description': gallery_item.description,
                    'category': gallery_item.category,
                    'image_count': len(gallery_images),
                    'main_image_url': gallery_images[0]['image_url'] if gallery_images else None,
                    'images': gallery_images,
                    'order': gallery_item.order,
                    'is_active': gallery_item.is_active,
                    'created_at': gallery_item.created_at.strftime('%d.%m.%Y %H:%M')
                }
            })

        except Gallery.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Galerie-Eintrag nicht gefunden.'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Fehler beim Aktualisieren: {str(e)}'
            })

    return JsonResponse({'success': False, 'message': 'Nur POST erlaubt.'})


@user_passes_test(lambda u: u.is_superuser)
@csrf_exempt
def admin_gallery_delete(request, gallery_id):
    """
    AJAX endpoint zum Löschen eines Galerie-Eintrags und aller seiner Bilder
    """
    if request.method == 'DELETE':
        try:
            gallery_item = Gallery.objects.get(id=gallery_id)

            # Alle Bilder löschen
            for gallery_image in gallery_item.images.all():
                default_storage.delete(gallery_image.image.path)
                gallery_image.delete()

            gallery_item.delete()

            return JsonResponse({
                'success': True,
                'message': 'Galerie-Eintrag wurde erfolgreich gelöscht.'
            })

        except Gallery.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Galerie-Eintrag nicht gefunden.'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Fehler beim Löschen: {str(e)}'
            })

    return JsonResponse({'success': False, 'message': 'Nur DELETE erlaubt.'})


@user_passes_test(lambda u: u.is_superuser)
@csrf_exempt
def admin_gallery_toggle_active(request, gallery_id):
    """
    AJAX endpoint zum Aktivieren/Deaktivieren eines Galerie-Bildes
    """
    if request.method == 'POST':
        try:
            gallery_item = Gallery.objects.get(id=gallery_id)
            
            # Toggle the active status
            gallery_item.is_active = not gallery_item.is_active
            gallery_item.save()
            
            return JsonResponse({
                'success': True,
                'message': f'Bild wurde {"aktiviert" if gallery_item.is_active else "deaktiviert"}.',
                'is_active': gallery_item.is_active
            })
            
        except Gallery.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Bild nicht gefunden.'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Fehler beim Aktualisieren: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Nur POST erlaubt.'})


@user_passes_test(lambda u: u.is_superuser)
@csrf_exempt
def admin_gallery_data(request, gallery_id):
    """
    AJAX endpoint zum Laden der Galerie-Daten für das Edit-Modal
    """
    if request.method == 'GET':
        try:
            gallery_item = Gallery.objects.get(id=gallery_id)
            
            images = []
            for img in gallery_item.images.all():
                images.append({
                    'id': img.id,
                    'image_url': img.image.url,
                    'order': img.order
                })
            
            return JsonResponse({
                'success': True,
                'gallery': {
                    'id': gallery_item.id,
                    'title': gallery_item.title,
                    'description': gallery_item.description,
                    'category': gallery_item.category,
                    'order': gallery_item.order,
                    'is_active': gallery_item.is_active,
                    'images': images
                }
            })
            
        except Gallery.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Galerie-Eintrag nicht gefunden.'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Fehler beim Laden: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Nur GET erlaubt.'})