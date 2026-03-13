from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task
from projects.models import Project
from accounts.models import User
from django.db.models import Count, Q
from django.utils import timezone


@login_required
def tache_create(request, projet_pk):
    projet = get_object_or_404(Project, pk=projet_pk)

    if request.user != projet.createur:
        messages.error(request, 'Seul le créateur peut ajouter des tâches !')
        return redirect('projet_detail', pk=projet_pk)

    if request.method == 'POST':
        titre = request.POST.get('titre')
        description = request.POST.get('description')
        date_limite = request.POST.get('date_limite') or None
        assignee_id = request.POST.get('assignee') or None

        assignee = None
        if assignee_id:
            assignee = get_object_or_404(User, pk=assignee_id)
            if request.user.is_etudiant() and assignee.is_professeur():
                messages.error(request, 'Un étudiant ne peut pas assigner un professeur !')
                return redirect('projet_detail', pk=projet_pk)

        Task.objects.create(
            titre=titre,
            description=description,
            projet=projet,
            assignee=assignee,
            date_limite=date_limite,
            priorite=request.POST.get('priorite', 'moyenne'),
        )
        messages.success(request, 'Tâche créée !')
        return redirect('projet_detail', pk=projet_pk)

    membres = projet.membres.all()
    return render(request, 'tasks/create.html', {'projet': projet, 'membres': membres})

@login_required
def tache_edit(request, pk):
    tache = get_object_or_404(Task, pk=pk)
    projet = tache.projet

    if request.user != projet.createur:
        messages.error(request, 'Accès refusé !')
        return redirect('projet_detail', pk=projet.pk)

    if request.method == 'POST':
        tache.titre = request.POST.get('titre')
        tache.description = request.POST.get('description')
        tache.date_limite = request.POST.get('date_limite') or None
        tache.statut = request.POST.get('statut')
        tache.priorite = request.POST.get('priorite', 'moyenne')
        assignee_id = request.POST.get('assignee') or None
        if assignee_id:
            assignee = get_object_or_404(User, pk=assignee_id)
            if request.user.is_etudiant() and assignee.is_professeur():
                messages.error(request, 'Un étudiant ne peut pas assigner un professeur !')
                return redirect('projet_detail', pk=projet.pk)
            tache.assignee = assignee
        else:
            tache.assignee = None
        tache.save()
        messages.success(request, 'Tâche modifiée !')
        return redirect('projet_detail', pk=projet.pk)

    membres = projet.membres.all()
    return render(request, 'tasks/edit.html', {'tache': tache, 'membres': membres})

@login_required
def tache_delete(request, pk):
    tache = get_object_or_404(Task, pk=pk)
    projet = tache.projet
    if request.user == projet.createur:
        tache.delete()
        messages.success(request, 'Tâche supprimée !')
    return redirect('projet_detail', pk=projet.pk)

@login_required
def tache_statut(request, pk):
    tache = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        nouveau_statut = request.POST.get('statut')
        tache.statut = nouveau_statut
        if nouveau_statut == 'termine':
            from django.utils import timezone
            tache.date_fin_reelle = timezone.now()
        tache.save()
        messages.success(request, 'Statut mis à jour !')
    return redirect('projet_detail', pk=tache.projet.pk)




@login_required
def statistiques(request):
    from projects.models import Project

    projets = Project.objects.filter(
        membres=request.user
    ) | Project.objects.filter(createur=request.user)
    projets = projets.distinct()

    stats_projets = []
    for projet in projets:
        taches = projet.taches.all()
        total = taches.count()
        terminees = taches.filter(statut='termine').count()
        dans_delais = sum(1 for t in taches if t.est_termine_dans_delais())
        en_retard = terminees - dans_delais

        prime = 0
        if total > 0:
            taux = dans_delais / total * 100
            if taux == 100:
                prime = 100000
            elif taux >= 90:
                prime = 30000

        stats_projets.append({
            'projet': projet,
            'total': total,
            'terminees': terminees,
            'dans_delais': dans_delais,
            'en_retard': en_retard,
            'taux': round(dans_delais / total * 100, 1) if total > 0 else 0,
            'prime': prime,
        })

    annee_courante = timezone.now().year
    trimestre_courant = (timezone.now().month - 1) // 3 + 1

    return render(request, 'tasks/statistiques.html', {
        'stats_projets': stats_projets,
        'annee_courante': annee_courante,
        'trimestre_courant': trimestre_courant,
    })

from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def envoyer_alertes(request):
    from .emails import envoyer_alertes_deadline
    envoyer_alertes_deadline()
    messages.success(request, 'Alertes email envoyées !')
    return redirect('dashboard')