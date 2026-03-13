from django.urls import path
from . import views

urlpatterns = [
    path('', views.projet_liste, name='projet_liste'),
    path('projet/create/', views.projet_create, name='projet_create'),
    path('projet/<int:pk>/', views.projet_detail, name='projet_detail'),
    path('projet/<int:pk>/edit/', views.projet_edit, name='projet_edit'),
    path('projet/<int:pk>/delete/', views.projet_delete, name='projet_delete'),
    path('projet/<int:pk>/membres/', views.projet_membres, name='projet_membres'),
    path('projet/<int:pk>/membres/ajouter/', views.projet_ajouter_membre, name='projet_ajouter_membre'),
    path('projet/<int:pk>/membres/retirer/<int:user_pk>/', views.projet_retirer_membre, name='projet_retirer_membre'),
    path('<int:pk>/kanban/', views.projet_kanban, name='projet_kanban'),
]