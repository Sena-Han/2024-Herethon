from django.db import models

from accounts.models import CustomUser


class Advice(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField(max_length=500)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(CustomUser, related_name='liked_advices', blank=True)

    def like_count(self):
        return self.likes.count()
