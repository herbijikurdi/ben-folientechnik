from django.shortcuts import render, redirect
from django.db.models import Count
from reviews.models import Review
from django.db.models import Avg
from django.core.mail import send_mail

def index(request):
    return render(request, 'index.html')

def impressum(request):
    return render(request, 'impressum.html')

def galerie(request):
    return render(request, 'galerie.html')

def bewertungen(request):
    return render(request, 'bewertungen.html')

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
            recipient_list=['benfolientechnik@gmail.com'],
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

        Review.objects.create(
            name=name,
            email=email,
            service=service,
            rating=rating,
            comment=comment
        )
        return redirect('bewertungerfolgreich')

    reviews = Review.objects.order_by('-created_at')
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

    context = {
        'reviews': reviews,
        'total_reviews': total_reviews,
        'rating_percentages': rating_percentages,
        'average_rating': average_rating,
        'average_rating_rounded': average_rating_rounded,
    }
    return render(request, 'bewertungen.html', context)