from rest_framework import serializers
from .models import Project
from accounts.serializers import UserSerializer

class ProjectSerializer(serializers.ModelSerializer):
    createur = UserSerializer(read_only=True)
    membres = UserSerializer(many=True, read_only=True)
    nombre_taches = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'titre', 'description', 'createur', 'membres', 'nombre_taches', 'date_creation']
        read_only_fields = ['id', 'createur', 'date_creation']

    def get_nombre_taches(self, obj):
        return obj.taches.count()

    def create(self, validated_data):
        projet = Project.objects.create(
            createur=self.context['request'].user,
            **validated_data
        )
        projet.membres.add(self.context['request'].user)
        return projet