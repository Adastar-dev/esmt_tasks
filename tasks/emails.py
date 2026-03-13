from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import Task

def envoyer_alertes_deadline():
    aujourd_hui = timezone.now().date()
    dans_3_jours = aujourd_hui + timezone.timedelta(days=3)

    taches = Task.objects.filter(
        statut__in=['todo', 'en_cours'],
        date_limite__lte=dans_3_jours,
        date_limite__gte=aujourd_hui,
        assignee__isnull=False
    )

    for tache in taches:
        if tache.assignee.email:
            jours_restants = (tache.date_limite - aujourd_hui).days
            sujet = f"⏰ Deadline approche — {tache.titre}"
            message = f"""
Bonjour {tache.assignee.username},

La tâche "{tache.titre}" du projet "{tache.projet.titre}" 
arrive à échéance dans {jours_restants} jour(s) !

Date limite : {tache.date_limite.strftime('%d/%m/%Y')}
Statut actuel : {tache.get_statut_display()}

Connectez-vous sur ESMT Tasks pour mettre à jour votre tâche.

— L'équipe ESMT Tasks 🌸
            """
            send_mail(
                sujet,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [tache.assignee.email],
                fail_silently=False,
            )
            print(f"Email envoyé à {tache.assignee.email} pour {tache.titre}")