from django.db import models

# Create your models here.
class Photo(models.Model):
    image = models.ImageField(null=False, blank=False, upload_to="images/")

