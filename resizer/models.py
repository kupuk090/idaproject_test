from django.db import models


class Image(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)
    image = models.ImageField(upload_to='images')
    uploaded_at = models.DateTimeField(auto_now_add=True)
