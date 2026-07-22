from django.db import models

# Create your models here.
class ServerConfig(models.Model):
    """server config model definition for websocket url"""
    websocket_url = models.URLField()
    updated_at = models.DateTimeField(auto_now=True)
