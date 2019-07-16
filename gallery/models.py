import re

from django.db import models
from django.utils.text import Truncator

from datetime import date
# Get current user
from django.contrib.auth import get_user_model

# For saving thumbnails
from PIL import Image as PIL_Image
from django.core.files.base import ContentFile
from io import BytesIO
import os.path

SHORT_TEXT = 50
VERY_SHORT_TEXT = 20 

# Create your models here.
class Board(models.Model):
    name        = models.CharField(max_length=20, unique=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=100, default='')
    
    def __str__(self):
        return self.name

class Thread(models.Model):
    board       = models.ForeignKey(Board, on_delete=models.CASCADE, null=False)

    def __str__(self):
        try:
            text = Post.objects.filter(thread__id=self.pk).first().text
            # TODO: why doesn't this work correctly?
#             return Truncator(text).chars(3)
            return text
        except:
            return 'NO_FIRST_POST_FOUND'

    # Helper functions
    def created_at(self):
        try:
            return Post.objects.filter(thread__id=self.pk).first().created_at
        except:
            return date.today()
    
    def updated_at(self):
        try:
            return Post.objects.filter(thread__id=self.pk).first().updated_at
        except:
            return date.today()

    def all_posts(self):
        return Post.objects.filter(thread__id=self.pk)

    def first_post(self):
        return Post.objects.filter(thread__id=self.pk).first()
    
    def last_post(self):
        return Post.objects.filter(thread__id=self.pk).last()

class Post(models.Model):
    created_at  = models.DateTimeField(auto_now_add=True)
    original    = models.ImageField(upload_to = 'img', blank=True)
    thumbnail   = models.ImageField(upload_to = 'tmb', editable=False, blank=True)
    text        = models.TextField()
    thread      = models.ForeignKey(Thread, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.make_thumbnail():
            raise Exception("Unable to create thumbnail.")
        
        super(Post, self).save(*args, **kwargs)
        
        self.make_replies()

    # Collect all IDs that start with ">>". Do regex in two parts since it's difficult 
    # to craft it in to a single regex.
    def make_replies(self):

        # Match reply IDs as "word boundaries".
        # Example: text ">>213 >>12" returns [>>213, >>12]
        regex = '(^|\W)>>\d{1,11}'
        pattern = re.compile(regex)
       
        # Filter out numbers.
        # Example: text ">>213" returns "213"
        regex_numbers = '(?<=>>)\d{1,11}'
        pattern_numbers = re.compile(regex_numbers)

        # Populate Reply table. Filter unique numbers using set.
        unique_ids = set()
        for numbers in re.finditer(regex, self.text):
            filtered_num = re.search(pattern_numbers, numbers.group(0)).group(0)
            unique_ids.add(int(filtered_num))

        for uid in unique_ids:
            reply = Reply(to_post=Post.objects.get(pk=uid), from_post=self)
            reply.save()

    # Create thumbnail from the original Image
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
        return Truncator(self.text).chars(VERY_SHORT_TEXT)

    def short_text(self):
        return Truncator(self.text).chars(SHORT_TEXT)
    
    def very_short_text(self):
        return Truncator(self.text).chars(VERY_SHORT_TEXT)

    def get_replies(self):
        return Reply.objects.filter(to_post=self.pk)

class Reply(models.Model):
    to_post     = models.ForeignKey(Post, on_delete=models.CASCADE, 
            null=True, related_name='to_post')
    from_post   = models.ForeignKey(Post, on_delete=models.CASCADE, 
            null=True, related_name='from_post')
