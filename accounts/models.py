from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class UserAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='account')
    phone = models.CharField(max_length=20)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    address = models.CharField(max_length=100)
    birthday = models.DateField(null=True, blank=True)
    def __str__(self):
        return self.user.username