from django.db import models
from django.contrib.auth.models import User

class Niche(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class GeneratedNewsletter(models.Model):
    niche = models.ForeignKey(Niche, related_name='newsletters', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Newsletter for {self.niche.name} at {self.created_at.strftime('%Y-%m-%d')}"
