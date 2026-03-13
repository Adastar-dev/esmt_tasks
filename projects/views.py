from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project
from accounts.models import User


@login_required
def projet_liste(request):
    projets = Project.objects.filter(membres=request.user) | Project.objects.filter(createur=request.user)
    projets = projets.distinct()
    return render(request, 'projects/liste.html', {'projets': projets})

@login_required
def projet_create(request):
    if request.method == 'POST':
        titre = request.POST.get('titre')
        description = request.POST.get('description')
        projet = Project.objects.create(
            titre=titre,
            description=description,
            createur=request.user
        )
        projet.membres.add(request.user)
        messages.success(request, 'Projet créé avec succès !')
        return redirect('projet_detail', pk=projet.pk)
    return render(request, 'projects/create.html')

@login_required
def projet_detail(request, pk):
    projet = get_object_or_404(Project, pk=pk)
    taches = projet.taches.all()

    statut_actif = request.GET.get('statut', '')
    priorite_actif = request.GET.get('priorite', '')
    assignee_actif = request.GET.get('assignee', '')

    if statut_actif:
        taches = taches.filter(statut=statut_actif)
    if priorite_actif:
        taches = taches.filter(priorite=priorite_actif)
    if assignee_actif:
        taches = taches.filter(assignee__pk=assignee_actif)

    statuts = [
        ('', 'Tous'),
        ('todo', 'À faire'),
        ('en_cours', 'En cours'),
        ('termine', 'Terminé'),
    ]
    priorites = [
        ('', 'Toutes'),
        ('basse', '🟢 Basse'),
        ('moyenne', '🟡 Moyenne'),
        ('haute', '🔴 Haute'),
    ]

    return render(request, 'projects/detail.html', {
        'projet': projet,
        'taches': taches,
        'statuts': statuts,
        'priorites': priorites,
        'statut_actif': statut_actif,
        'priorite_actif': priorite_actif,
        'assignee_actif': assignee_actif,
    })

@login_required
def projet_edit(request, pk):
    projet = get_object_or_404(Project, pk=pk)
    if request.user != projet.createur:
        messages.error(request, 'Accès refusé !')
        return redirect('projet_liste')
    if request.method == 'POST':
        projet.titre = request.POST.get('titre')
        projet.description = request.POST.get('description')
        projet.save()
        messages.success(request, 'Projet modifié !')
        return redirect('projet_detail', pk=projet.pk)
    return render(request, 'projects/edit.html', {'projet': projet})

@login_required
def projet_delete(request, pk):
    projet = get_object_or_404(Project, pk=pk)
    if request.user == projet.createur:
        projet.delete()
        messages.success(request, 'Projet supprimé !')
    return redirect('projet_liste')


@login_required
def projet_membres(request, pk):
    projet = get_object_or_404(Project, pk=pk)
    if request.user != projet.createur:
        messages.error(request, 'Accès refusé !')
        return redirect('projet_detail', pk=pk)
    users_disponibles = User.objects.exclude(pk=projet.createur.pk)
    if request.user.role == 'etudiant':
        users_disponibles = users_disponibles.filter(role='etudiant')

    return render(request, 'projects/membres.html', {
        'projet': projet,
        'users_disponibles': users_disponibles
    })

@login_required
def projet_ajouter_membre(request, pk):
    projet = get_object_or_404(Project, pk=pk)
    if request.user != projet.createur:
        messages.error(request, 'Accès refusé !')
        return redirect('projet_detail', pk=pk)
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = get_object_or_404(User, pk=user_id)

        if request.user.role == 'etudiant' and user.role == 'professeur':
            messages.error(request, 'Un étudiant ne peut pas ajouter un professeur à son projet !')
            return redirect('projet_membres', pk=pk)

        projet.membres.add(user)
        messages.success(request, f'{user.username} ajouté au projet !')
    return redirect('projet_membres', pk=pk)

@login_required
def projet_retirer_membre(request, pk, user_pk):
    projet = get_object_or_404(Project, pk=pk)
    if request.user != projet.createur:
        messages.error(request, 'Accès refusé !')
        return redirect('projet_detail', pk=pk)
    user = get_object_or_404(User, pk=user_pk)
    projet.membres.remove(user)
    messages.success(request, f'{user.username} retiré du projet !')
    return redirect('projet_membres', pk=pk)

@login_required
def projet_kanban(request, pk):
    from django.utils import timezone
    projet = get_object_or_404(Project, pk=pk)
    colonne_data = [
        {
            'id': 'todo',
            'titre': 'À faire',
            'emoji': '📋',
            'color': '#888',
            'bg': '#f5f5f5',
            'taches': projet.taches.filter(statut='todo'),
        },
        {
            'id': 'en_cours',
            'titre': 'En cours',
            'emoji': '⚡',
            'color': '#e08a00',
            'bg': '#fff3e0',
            'taches': projet.taches.filter(statut='en_cours'),
        },
        {
            'id': 'termine',
            'titre': 'Terminé',
            'emoji': '✅',
            'color': '#4caf50',
            'bg': '#e8f5e9',
            'taches': projet.taches.filter(statut='termine'),
        },
    ]
    return render(request, 'projects/kanban.html', {
        'projet': projet,
        'colonne_data': colonne_data,
        'today': timezone.now().date(),
    })