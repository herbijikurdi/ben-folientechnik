from django.db import models

class Review(models.Model):
    SERVICE_CHOICES = [
        ('folierung', 'Fahrzeugfolierung'),
        ('beschriftung', 'Werbebeschriftung'),
        ('scheibentoenung', 'Scheibentönung'),
        ('sonstiges', 'Sonstiges'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Wartend'),
        ('approved', 'Genehmigt'),
        ('rejected', 'Abgelehnt'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.rating} Sterne) - {self.get_status_display()}"


class Gallery(models.Model):
    CATEGORY_CHOICES = [
        ('folierung', 'Fahrzeugfolierung'),
        ('beschriftung', 'Werbebeschriftung'),
        ('scheibentoenung', 'Scheibentönung'),
        ('sonstiges', 'Sonstiges'),
    ]

    title = models.CharField(max_length=200, help_text="Titel des Galerie-Bildes")
    description = models.TextField(blank=True, help_text="Optionale Beschreibung")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='folierung', help_text="Kategorie des Projekts")
    order = models.PositiveIntegerField(default=0, help_text="Reihenfolge (kleinere Zahlen zuerst)")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, help_text="Bild in Galerie anzeigen")

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Galerie-Bild"
        verbose_name_plural = "Galerie-Bilder"

    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"

    @property
    def main_image(self):
        """Gibt das erste Bild zurück oder None"""
        return self.images.first()

    @property
    def image_count(self):
        """Gibt die Anzahl der Bilder zurück"""
        return self.images.count()


class GalleryImage(models.Model):
    gallery = models.ForeignKey(Gallery, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='gallery/', help_text="Bild hochladen")
    order = models.PositiveIntegerField(default=0, help_text="Reihenfolge innerhalb der Galerie (kleinere Zahlen zuerst)")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = "Galerie-Bild"
        verbose_name_plural = "Galerie-Bilder"

    def __str__(self):
        return f"Bild {self.order} von {self.gallery.title}"