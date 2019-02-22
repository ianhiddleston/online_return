from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from character.models import *

class CharacterCreate(forms.ModelForm):
    class Meta:
        model = Character
        fields = ('name', 'race', 'nationality', 'languages', 'guilds', 'notes')
