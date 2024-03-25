from django.db import models
from django.utils import timezone
# Create your models here.
class Sites(models.Model):
    url = models.URLField(null=False, blank=False, unique=True)
    json = models.JSONField(blank=False, null=False)
    last_modified = models.DateTimeField(auto_now=True, blank=False, null=False)
    class Meta:
        verbose_name_plural = 'data'
    def __str__(self):
        return f"{self.url}"