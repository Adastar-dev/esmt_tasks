from django.urls import path
from . import views

urlpatterns = [
    path('projet/<int:projet_pk>/tache/create/', views.tache_create, name='tache_create'),
    path('tache/<int:pk>/edit/', views.tache_edit, name='tache_edit'),
    path('tache/<int:pk>/delete/', views.tache_delete, name='tache_delete'),
    path('tache/<int:pk>/statut/', views.tache_statut, name='tache_statut'),
    path('statistiques/', views.statistiques, name='statistiques'),
    path('alertes/envoyer/', views.envoyer_alertes, name='envoyer_alertes'),
]
