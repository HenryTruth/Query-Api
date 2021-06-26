from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = CloudinaryField('image')
    bio = models.TextField(max_length=100, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)

    #     img = Image.open(self.image.path)

    #     if img.height > 300 or img.width > 300:
    #         output_size = (300,300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)


    @property
    def owner(self):
        return self.user




