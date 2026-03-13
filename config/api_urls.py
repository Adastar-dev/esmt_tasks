from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from accounts.api_views import RegisterView, LoginView, MeView, UserListView
from projects.api_views import ProjectListCreateView, ProjectDetailView, ProjectMembresView
from tasks.api_views import TaskListCreateView, TaskDetailView, TaskStatutView, StatistiquesView

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='api_register'),
    path('auth/login/', LoginView.as_view(), name='api_login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='api_refresh'),
    path('auth/me/', MeView.as_view(), name='api_me'),
    path('users/', UserListView.as_view(), name='api_users'),

    path('projets/', ProjectListCreateView.as_view(), name='api_projets'),
    path('projets/<int:pk>/', ProjectDetailView.as_view(), name='api_projet_detail'),
    path('projets/<int:pk>/membres/', ProjectMembresView.as_view(), name='api_projet_membres'),

    path('projets/<int:projet_pk>/taches/', TaskListCreateView.as_view(), name='api_taches'),
    path('taches/<int:pk>/', TaskDetailView.as_view(), name='api_tache_detail'),
    path('taches/<int:pk>/statut/', TaskStatutView.as_view(), name='api_tache_statut'),

    path('statistiques/', StatistiquesView.as_view(), name='api_statistiques'),
]