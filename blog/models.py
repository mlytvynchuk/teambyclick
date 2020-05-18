from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


class Post(models.Model):
    title = models.CharField(max_length=150)
    short_description = models.TextField()
    content = RichTextUploadingField()
    posted_at = models.DateField(auto_now_add=True)
