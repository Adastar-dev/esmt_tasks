from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    auteur_username = serializers.CharField(source='auteur.username', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'auteur_username', 'contenu', 'date_envoi']