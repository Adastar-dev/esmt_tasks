from django.db import models
from accounts.models import User
from projects.models import Project

class Message(models.Model):
    projet = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='messages')
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    contenu = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.auteur.username}: {self.contenu[:50]}"

    class Meta:
        ordering = ['date_envoi']