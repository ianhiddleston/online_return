from django.contrib.auth import login, authenticate
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from character.models import Player
from signup.forms import SignUpForm, ProfileForm

def signup(request):
    if request.method == 'POST':
        # Verify form and that user does not already exist.
        user_form = SignUpForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.refresh_from_db()
            profile_form = ProfileForm(request.POST, instance=user.player)  # Reload the profile form with the profile instance
            if profile_form.is_valid():
              profile_form.save()
            group = Group.objects.get(name='Users')
            user.groups.add(group)
            username = user_form.cleaned_data.get('username')
            raw_password = user_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/character/')
    else:
        user_form = SignUpForm()
        profile_form = ProfileForm()
    return render(request, 'signup.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
