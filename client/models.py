from django.utils import timezone
from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=150)
    dni = models.CharField(max_length=12, unique=True)
    celphone = models.CharField(max_length=15)
    address = models.CharField(max_length=200)
    observation = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='client', blank=True, null=True )
    active_membership = models.BooleanField(default=False)
    active_until = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    def is_membership_active(self):
        """Check if the membership is currently active."""
        if self.active_membership and self.active_until:
            return self.active_until >= timezone.now().date()
        return False