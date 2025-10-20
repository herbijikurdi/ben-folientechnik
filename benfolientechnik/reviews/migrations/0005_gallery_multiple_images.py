# Generated manually for multiple images support

from django.db import migrations, models
import django.db.models.deletion


def migrate_existing_images(apps, schema_editor):
    Gallery = apps.get_model('reviews', 'Gallery')
    GalleryImage = apps.get_model('reviews', 'GalleryImage')

    for gallery in Gallery.objects.filter(image__isnull=False):
        GalleryImage.objects.create(
            gallery=gallery,
            image=gallery.image,
            order=0
        )


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_gallery_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='GalleryImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(help_text='Bild hochladen', upload_to='gallery/')),
                ('order', models.PositiveIntegerField(default=0, help_text='Reihenfolge innerhalb der Galerie (kleinere Zahlen zuerst)')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('gallery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='reviews.gallery')),
            ],
            options={
                'verbose_name': 'Galerie-Bild',
                'verbose_name_plural': 'Galerie-Bilder',
                'ordering': ['order', 'created_at'],
            },
        ),
        # Migrate existing images to GalleryImage
        migrations.RunPython(migrate_existing_images, reverse_code=migrations.RunPython.noop),
        # Remove the old image field
        migrations.RemoveField(
            model_name='gallery',
            name='image',
        ),
    ]