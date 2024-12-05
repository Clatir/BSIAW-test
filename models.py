from django.db import models

# Create your models here.

class VideoClip(models.Model):
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=500) 
    video_source = models.FileField(upload_to="video/%y") 

    def __str__(self):
        return self.name