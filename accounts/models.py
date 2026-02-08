from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    height_cm = models.FloatField(null=True, blank=True, help_text='Height in centimeters')
    weight_kg = models.FloatField(null=True, blank=True, help_text='Weight in kilograms')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def bmi(self):
        if self.height_cm and self.weight_kg:
            height_m = self.height_cm / 100
            return self.weight_kg / (height_m ** 2)
        return None
