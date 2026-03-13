from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Project
from .serializers import ProjectSerializer
from accounts.models import User

class ProjectListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return (Project.objects.filter(membres=user) | Project.objects.filter(createur=user)).distinct()

class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return (Project.objects.filter(membres=user) | Project.objects.filter(createur=user)).distinct()

    def update(self, request, *args, **kwargs):
        projet = self.get_object()
        if request.user != projet.createur:
            return Response({'error': 'Accès refusé'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        projet = self.get_object()
        if request.user != projet.createur:
            return Response({'error': 'Accès refusé'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

class ProjectMembresView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        projet = Project.objects.get(pk=pk)
        if request.user != projet.createur:
            return Response({'error': 'Accès refusé'}, status=status.HTTP_403_FORBIDDEN)
        user_id = request.data.get('user_id')
        user = User.objects.get(pk=user_id)

        if request.user.role == 'etudiant' and user.role == 'professeur':
            return Response({'error': 'Un étudiant ne peut pas ajouter un professeur à son projet.'},
                            status=status.HTTP_403_FORBIDDEN)

        projet.membres.add(user)
        return Response({'message': f'{user.username} ajouté !'})

    def delete(self, request, pk):
        projet = Project.objects.get(pk=pk)
        if request.user != projet.createur:
            return Response({'error': 'Accès refusé'}, status=status.HTTP_403_FORBIDDEN)
        user_id = request.data.get('user_id')
        user = User.objects.get(pk=user_id)
        projet.membres.remove(user)
        return Response({'message': f'{user.username} retiré !'})