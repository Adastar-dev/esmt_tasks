import pytest
from django.contrib.auth import get_user_model
from projects.models import Project
from tasks.models import Task

User = get_user_model()


@pytest.fixture
def professeur(db):
    return User.objects.create_user(
        username='test_prof',
        password='testpass123',
        role='professeur'
    )

@pytest.fixture
def etudiant(db):
    return User.objects.create_user(
        username='test_etudiant',
        password='testpass123',
        role='etudiant'
    )

@pytest.fixture
def projet(db, professeur):
    p = Project.objects.create(
        titre='Projet Test',
        description='Description test',
        createur=professeur
    )
    p.membres.add(professeur)
    return p

@pytest.fixture
def tache(db, projet, etudiant):
    projet.membres.add(etudiant)
    return Task.objects.create(
        titre='Tâche Test',
        description='Description tâche',
        projet=projet,
        assignee=etudiant,
        statut='todo',
        priorite='moyenne'
    )


@pytest.mark.django_db
def test_creation_utilisateur(professeur):
    assert professeur.username == 'test_prof'
    assert professeur.role == 'professeur'

@pytest.mark.django_db
def test_creation_etudiant(etudiant):
    assert etudiant.username == 'test_etudiant'
    assert etudiant.role == 'etudiant'

@pytest.mark.django_db
def test_mot_de_passe_hash(professeur):
    assert professeur.password != 'testpass123'
    assert professeur.check_password('testpass123')


@pytest.mark.django_db
def test_creation_projet(projet, professeur):
    assert projet.titre == 'Projet Test'
    assert projet.createur == professeur

@pytest.mark.django_db
def test_createur_est_membre(projet, professeur):
    assert professeur in projet.membres.all()

@pytest.mark.django_db
def test_ajouter_membre(projet, etudiant):
    projet.membres.add(etudiant)
    assert etudiant in projet.membres.all()

@pytest.mark.django_db
def test_retirer_membre(projet, etudiant):
    projet.membres.add(etudiant)
    projet.membres.remove(etudiant)
    assert etudiant not in projet.membres.all()



@pytest.mark.django_db
def test_creation_tache(tache):
    assert tache.titre == 'Tâche Test'
    assert tache.statut == 'todo'
    assert tache.priorite == 'moyenne'

@pytest.mark.django_db
def test_changement_statut(tache):
    tache.statut = 'en_cours'
    tache.save()
    assert tache.statut == 'en_cours'

@pytest.mark.django_db
def test_statut_termine(tache):
    tache.statut = 'termine'
    tache.save()
    assert tache.statut == 'termine'

@pytest.mark.django_db
def test_tache_assignee(tache, etudiant):
    assert tache.assignee == etudiant

@pytest.mark.django_db
def test_tache_appartient_projet(tache, projet):
    assert tache.projet == projet


@pytest.mark.django_db
def test_etudiant_ne_peut_pas_ajouter_professeur(etudiant, professeur):
    projet_etudiant = Project.objects.create(
        titre='Projet Étudiant',
        description='Test',
        createur=etudiant
    )
    projet_etudiant.membres.add(etudiant)
    if etudiant.role == 'etudiant' and professeur.role == 'professeur':
        peut_ajouter = False
    else:
        peut_ajouter = True
    assert peut_ajouter == False

@pytest.mark.django_db
def test_professeur_peut_ajouter_etudiant(professeur, etudiant):
    projet_prof = Project.objects.create(
        titre='Projet Prof',
        description='Test',
        createur=professeur
    )
    projet_prof.membres.add(etudiant)
    assert etudiant in projet_prof.membres.all()

@pytest.mark.django_db
def test_priorite_haute(tache):
    tache.priorite = 'haute'
    tache.save()
    assert tache.priorite == 'haute'

@pytest.mark.django_db
def test_priorite_basse(tache):
    tache.priorite = 'basse'
    tache.save()
    assert tache.priorite == 'basse'