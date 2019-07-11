from django.db import models

# Get current user
from django.contrib.auth import get_user_model

# For saving thumbnails
from PIL import Image as PIL_Image
from django.core.files.base import ContentFile
from io import BytesIO
import os.path

# Create your models here.
class Post(models.Model):
    created_at  = models.DateTimeField(auto_now_add=True)
    original    = models.ImageField(upload_to = 'img', blank=True)
    thumbnail   = models.ImageField(upload_to = 'tmb', editable=False, blank=True)
    caption     = models.CharField(max_length=49)
    text        = models.TextField()

    def save(self, *args, **kwargs):
        if not self.make_thumbnail():
            raise Exception("Unable to create thumbnail.")
        super(Post, self).save(*args, **kwargs)

    # Create thumbnail from original Image
    def make_thumbnail(self):

        # Image is optional
        if not self.original:
            return True

        image = PIL_Image.open(self.original)

        orig_size = image.size
        print("Image size:", orig_size)

        thumb_size = (250, 250)
        image.thumbnail(thumb_size, PIL_Image.ANTIALIAS)

        thumb_name, thumb_extension = os.path.splitext(self.original.name)
        thumb_extension = thumb_extension.lower()

        thumb_filename = thumb_name + '_thumb' + thumb_extension

        if thumb_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.gif':
            FTYPE = 'GIF'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        else:
            return False    # Unrecognized file type

        # Save thumbnail in-memory as StringIO file
        temp_thumb = BytesIO()
        image.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)

        # set save=False, otherwise it will run in an infinite loop
        self.thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()

        return True

    def __str__(self):
        return self.caption

class Thread(models.Model):
    title       = models.CharField(max_length=49)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now_add=True)
    post        = models.ManyToManyField(Post, blank=True)
    
    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.title
