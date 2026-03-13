from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Message
from projects.models import Project

@login_required
def chat_projet(request, projet_id):
    projet = get_object_or_404(Project, pk=projet_id)
    messages_anciens = Message.objects.filter(projet=projet).order_by('date_envoi')
    return render(request, 'chat/chat.html', {
        'projet': projet,
        'messages_anciens': messages_anciens,
    })