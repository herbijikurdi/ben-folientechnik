from django.shortcuts import render, redirect
from django.db.models import Count
from .models import Review

def reviews_page(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email", "")
        service = request.POST.get("service")
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")

        Review.objects.create(
            name=name,
            email=email,
            service=service,
            rating=rating,
            comment=comment
        )
        print(name, email, service, rating, comment)
        return redirect('reviews_page')

    reviews = Review.objects.order_by('-created_at')
    total_reviews = reviews.count()

    # Anzahl Bewertungen pro Stern
    rating_counts = reviews.values('rating').annotate(count=Count('rating')).order_by('rating')
    rating_dict = {entry['rating']: entry['count'] for entry in rating_counts}

    rating_percentages = {}
    for i in range(1, 6):
        count = rating_dict.get(i, 0)
        percent = (count / total_reviews * 100) if total_reviews > 0 else 0
        rating_percentages[i] = round(percent)

    context = {
        'reviews': reviews,
        'total_reviews': total_reviews,
        'rating_percentages': rating_percentages,
    }
    return render(request, 'bewertungen.html', context)