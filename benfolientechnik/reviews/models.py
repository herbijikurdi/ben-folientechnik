from django.db import models

class Review(models.Model):
    SERVICE_CHOICES = [
        ('folierung', 'Fahrzeugfolierung'),
        ('beschriftung', 'Werbebeschriftung'),
        ('scheibentoenung', 'Scheibentönung'),
        ('sonstiges', 'Sonstiges'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.rating} Sterne)"