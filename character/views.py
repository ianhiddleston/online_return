from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from character.models import Character, Player
from character.forms import CharacterCreate

# Create your views here.

def index(request):
    return render(request, 'index.html')

@login_required
def player(request):
    return HttpResponse("Hello world. You're in the Character module looking at your player details.")

@login_required
def list(request):
    #Get user Player details
    current_player = request.user.player
    characters =  Character.objects.filter(player=current_player)
    current_characters = characters.filter(state=Character.ACTIVE)
    previous_characters = characters.exclude(state=Character.ACTIVE)
    context = {'current_characters': current_characters, 'previous_characters': previous_characters}
    return render(request, 'list.html', context)

@login_required
def details(request, character_id):
    character = get_object_or_404(Character, pk=character_id)
    if character.player.user != request.user:
        return HttpResponse('Unauthorized', status=401)
    return render(request, 'details.html', {'character': character})

@login_required
def create_character(request):
    if request.method == 'POST':
        #Need to split these up, manytomany won't work until the character has a primary_key
        character_form = CharacterCreate(request.POST)
        if character_form.is_valid():
            character = character_form.save(commit=False)
            character.player = request.user.player
            for guild in character.guilds:
                #Add the starting guild rank for each guild picked at creation.
                character.guild_ranks.add(guild.starting_rank())
            character.save()
            return redirect('/character/')
    else:
        #Can't create a character if you have an active character.
        current_player = Player.objects.get(user=request.user)
        characters =  Character.objects.filter(player=current_player).filter(state=Character.ACTIVE).count()
        if characters > 0:
            return HttpResponse('Unauthorized: You have a currently active character.', status=401)
        else:
            character_form = CharacterCreate()
    return render(request, 'create.html', {
        'character_form': character_form,
    })
