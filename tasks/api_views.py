from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from .models import Task
from .serializers import TaskSerializer
from projects.models import Project

class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        projet_pk = self.kwargs.get('projet_pk')
        return Task.objects.filter(projet__pk=projet_pk)

    def perform_create(self, serializer):
        projet = Project.objects.get(pk=self.kwargs['projet_pk'])
        assignee_id = self.request.data.get('assignee_id')
        assignee = None
        if assignee_id:
            from accounts.models import User
            assignee = User.objects.get(pk=assignee_id)
        serializer.save(projet=projet, assignee=assignee)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

class TaskStatutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        tache = Task.objects.get(pk=pk)
        nouveau_statut = request.data.get('statut')
        tache.statut = nouveau_statut
        if nouveau_statut == 'termine':
            from django.utils import timezone
            tache.date_fin_reelle = timezone.now()
        else:
            tache.date_fin_reelle = None
        tache.save()
        return Response(TaskSerializer(tache).data)

class StatistiquesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        projets = (Project.objects.filter(membres=user) | Project.objects.filter(createur=user)).distinct()
        stats = []
        for projet in projets:
            taches = projet.taches.all()
            total = taches.count()
            terminees = taches.filter(statut='termine').count()
            dans_delais = sum(1 for t in taches if t.est_termine_dans_delais())
            taux = round(dans_delais / total * 100, 1) if total > 0 else 0
            prime = 0
            if taux == 100:
                prime = 100000
            elif taux >= 90:
                prime = 30000
            stats.append({
                'projet': projet.titre,
                'total': total,
                'terminees': terminees,
                'dans_delais': dans_delais,
                'taux': taux,
                'prime': prime,
            })
        return Response(stats)