# Revert to multiple images per gallery entry

from django.db import migrations, models


def migrate_single_images_to_gallery_images(apps, schema_editor):
    """Migrate single image back to GalleryImage objects"""
    Gallery = apps.get_model('reviews', 'Gallery')
    GalleryImage = apps.get_model('reviews', 'GalleryImage')

    for gallery in Gallery.objects.all():
        if gallery.image:  # If there's a single image
            # Create a GalleryImage for it
            GalleryImage.objects.create(
                gallery=gallery,
                image=gallery.image,
                order=0
            )


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0006_change_gallery_to_single_image'),
    ]

    operations = [
        # Create GalleryImage model again
        migrations.CreateModel(
            name='GalleryImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(help_text='Bild hochladen', upload_to='gallery/')),
                ('order', models.PositiveIntegerField(default=0, help_text='Reihenfolge innerhalb der Galerie (kleinere Zahlen zuerst)')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('gallery', models.ForeignKey(on_delete=models.CASCADE, related_name='images', to='reviews.gallery')),
            ],
            options={
                'verbose_name': 'Galerie-Bild',
                'verbose_name_plural': 'Galerie-Bilder',
                'ordering': ['order', 'created_at'],
            },
        ),
        # Migrate data from single image to GalleryImage
        migrations.RunPython(migrate_single_images_to_gallery_images),
        # Remove the single image field
        migrations.RemoveField(
            model_name='gallery',
            name='image',
        ),
    ]