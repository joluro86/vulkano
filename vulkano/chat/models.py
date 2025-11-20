from django.conf import settings
from django.db import models



class Room(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('active', 'Activa'),
        ('closed', 'Cerrada'),
    ]

    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='pending')
    started_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Usuario')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('timestamp',)

    def __str__(self):
        return f'{self.user}: {self.message[:20]}'
