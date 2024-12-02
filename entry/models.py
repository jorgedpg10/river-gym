from django.db import models

from client.models import Client


class Entry(models.Model):
    date_time = models.DateTimeField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return f"Entry for {self.client.name} on {self.date_time.strftime('%Y-%m-%d %H:%M:%S')}"
    
    class Meta:
        ordering = ['-date_time']