from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from character.models import Player, Branch

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class ProfileForm(forms.ModelForm):
    branch = forms.ModelChoiceField(queryset=Branch.objects.all(), empty_label="(Nothing)")
    first_aider = forms.TypedChoiceField(coerce=lambda x: x =='True',
                               choices=((False, 'No'), (True, 'Yes')))

    class Meta:
        model = Player
        fields = ('branch','phone_number', 'first_aider', 'emergency_contact_name', 'emergency_contact_number', 'emergency_contact_relationship')
