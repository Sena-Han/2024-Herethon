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
    start_year = models.IntegerField(null=True, blank=True)
    end_year = models.IntegerField(null=True, blank=True)

    # 임시로 넣어둔 부분입니다. 마이페이지 구현하시면서, 관리자 항목 입력 받는 부분 구현 완료되면 추가할 예정입니다.
    def is_currently_employed(self):
        return self.job_type is not None
