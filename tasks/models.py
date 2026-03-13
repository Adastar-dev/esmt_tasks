from django.db import models
from accounts.models import User
from projects.models import Project


class Task(models.Model):
    STATUT_CHOICES = [
        ('todo', 'À faire'),
        ('en_cours', 'En cours'),
        ('termine', 'Terminé'),
    ]
    PRIORITE_CHOICES = [
        ('basse', 'Basse'),
        ('moyenne', 'Moyenne'),
        ('haute', 'Haute'),
    ]

    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    projet = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='taches')
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='taches_assignees')
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='todo')
    priorite = models.CharField(max_length=10, choices=PRIORITE_CHOICES, default='moyenne')
    date_limite = models.DateField(null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_fin_reelle = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.titre} [{self.get_statut_display()}]"

    def est_termine_dans_delais(self):
        if self.statut == 'termine' and self.date_limite:
            return True
        return False