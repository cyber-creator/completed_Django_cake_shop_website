from django.db import models
from django.conf import settings

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=250, blank=True)
    phone_number = models.CharField(max_length=50, blank=True)
    email = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    postal_code = models.IntegerField(blank=True, null=True)
    city = models.CharField(max_length=250, blank=True, null=True)
    state = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return f'{self.email} profile'
