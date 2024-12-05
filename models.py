from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, default='user')
    phone = PhoneNumberField(null=True, blank = True)
    fa_key = models.BinaryField()  
    salt = models.BinaryField()

    def __str__(self):
        return self.user.email