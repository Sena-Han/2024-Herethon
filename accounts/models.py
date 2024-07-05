from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    username = models.CharField(max_length=30, unique=True)
    nickname = models.CharField(max_length=10)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    email_verified = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    job_type = models.CharField(max_length=50, null=True, blank=True)

class MyPage(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    start_year = models.IntegerField(null=True, blank=True)
    end_year = models.IntegerField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    is_employed = models.BooleanField(default=False)
    company_name = models.CharField(max_length=100, null=True, blank=True)
    position = models.CharField(max_length=100, null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)