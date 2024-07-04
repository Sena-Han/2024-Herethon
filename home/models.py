import os

from django.db import models

from accounts.models import CustomUser


class Advice(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField(max_length=500)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='photos_advice/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    scraps = models.ManyToManyField(CustomUser, related_name='scrapped_advices', blank=True)
    likes = models.ManyToManyField(CustomUser, related_name='liked_advices', blank=True)

    def like_count(self):
        return self.likes.count()

    def delete(self, *args, **kwargs):
        if self.photo:
            if os.path.isfile(self.photo.path):
                os.remove(self.photo.path)
        super().delete(*args, **kwargs)
