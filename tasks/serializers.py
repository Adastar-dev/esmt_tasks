from rest_framework import serializers
from .models import Task
from accounts.serializers import UserSerializer

class TaskSerializer(serializers.ModelSerializer):
    assignee = UserSerializer(read_only=True)
    assignee_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    statut_display = serializers.CharField(source='get_statut_display', read_only=True)
    dans_delais = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id', 'titre', 'description', 'projet', 'assignee', 'assignee_id',
            'statut', 'statut_display', 'date_limite', 'date_creation',
            'date_fin_reelle', 'dans_delais', 'priorite'
        ]
        read_only_fields = ['id', 'date_creation', 'projet']

    def get_dans_delais(self, obj):
        return obj.est_termine_dans_delais()

    def validate(self, data):
        request = self.context['request']
        assignee_id = data.get('assignee_id')
        if assignee_id:
            from accounts.models import User
            assignee = User.objects.get(pk=assignee_id)
            if request.user.is_etudiant() and assignee.is_professeur():
                raise serializers.ValidationError(
                    "Un étudiant ne peut pas assigner un professeur."
                )
        return data