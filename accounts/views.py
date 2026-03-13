from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import InscriptionForm, ProfilForm
from django.db.models import Q

def inscription(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Bienvenue {user.username} !')
            return redirect('dashboard')
        else:
            # Affiche les erreurs dans le terminal pour déboguer
            print("ERREURS FORMULAIRE:", form.errors)
    else:
        form = InscriptionForm()
    return render(request, 'accounts/inscription.html', {'form': form})

def connexion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Identifiants incorrects')
    return render(request, 'accounts/connexion.html')

@login_required
def deconnexion(request):
    logout(request)
    return redirect('connexion')

@login_required
def profil(request):
    if request.method == 'POST':
        form = ProfilForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil mis à jour !')
            return redirect('profil')
    else:
        form = ProfilForm(instance=request.user)
    return render(request, 'accounts/profil.html', {'form': form})

@login_required
def dashboard(request):
    from projects.models import Project
    from tasks.models import Task
    from django.utils import timezone

    projets = Project.objects.filter(membres=request.user) | Project.objects.filter(createur=request.user)
    projets = projets.distinct()

    # Notifications deadline
    aujourd_hui = timezone.now().date()
    dans_3_jours = aujourd_hui + timezone.timedelta(days=3)

    alertes = Task.objects.filter(
        Q(projet__membres=request.user) | Q(projet__createur=request.user),
        statut__in=['todo', 'en_cours'],
        date_limite__isnull=False,
        date_limite__lte=dans_3_jours,
    ).distinct().select_related('projet')

    alertes_retard = alertes.filter(date_limite__lt=aujourd_hui)
    alertes_proche = alertes.filter(date_limite__gte=aujourd_hui)

    return render(request, 'accounts/dashboard.html', {
        'projets': projets,
        'alertes_retard': alertes_retard,
        'alertes_proche': alertes_proche,
    })

@login_required
def recherche(request):
    query = request.GET.get('q', '')
    projets = []
    taches = []

    if query:
        from projects.models import Project
        from tasks.models import Task

        projets = Project.objects.filter(
            Q(titre__icontains=query) | Q(description__icontains=query)
        ).filter(
            Q(createur=request.user) | Q(membres=request.user)
        ).distinct()

        taches = Task.objects.filter(
            Q(titre__icontains=query) | Q(description__icontains=query)
        ).filter(
            Q(projet__createur=request.user) | Q(projet__membres=request.user)
        ).distinct()

    return render(request, 'accounts/recherche.html', {
        'query': query,
        'projets': projets,
        'taches': taches,
    })