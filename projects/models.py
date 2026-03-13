from django.db import models
from accounts.models import User

class Project(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    createur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projets_crees')
    membres = models.ManyToManyField(User, related_name='projets_membres', blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titre