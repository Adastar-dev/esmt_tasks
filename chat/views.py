from rest_framework import generics, permissions
from .models import Message
from .serializers import MessageSerializer
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from projects.models import Project

class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        projet_id = self.kwargs['projet_id']
        return Message.objects.filter(projet__pk=projet_id).order_by('date_envoi')

@login_required
def chat_projet(request, projet_id):
    projet = get_object_or_404(Project, pk=projet_id)
    messages_anciens = Message.objects.filter(projet=projet).order_by('date_envoi')
    return render(request, 'chat/chat.html', {
        'projet': projet,
        'messages_anciens': messages_anciens,
    })