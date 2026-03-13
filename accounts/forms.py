from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class InscriptionForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=[
        ('etudiant', 'Étudiant'),
        ('professeur', 'Professeur'),
    ])

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'role', 'password1', 'password2']

class ProfilForm(UserChangeForm):
    password = None  # On cache le champ password

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'avatar']