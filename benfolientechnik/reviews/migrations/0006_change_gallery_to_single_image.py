# Generated manually for changing Gallery model to single image

from django.db import migrations, models


def migrate_gallery_images(apps, schema_editor):
    """Migrate existing GalleryImage data to Gallery.image field"""
    Gallery = apps.get_model('reviews', 'Gallery')
    GalleryImage = apps.get_model('reviews', 'GalleryImage')

    for gallery in Gallery.objects.all():
        # Get the first image for each gallery
        first_image = GalleryImage.objects.filter(gallery=gallery).first()
        if first_image:
            gallery.image = first_image.image
            gallery.save()


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0005_gallery_multiple_images'),
    ]

    operations = [
        # Add image field to Gallery
        migrations.AddField(
            model_name='gallery',
            name='image',
            field=models.ImageField(default='', upload_to='gallery/', help_text='Bild hochladen'),
            preserve_default=False,
        ),
        # Migrate data from GalleryImage to Gallery
        migrations.RunPython(migrate_gallery_images),
        # Remove GalleryImage model
        migrations.DeleteModel(
            name='GalleryImage',
        ),
    ]