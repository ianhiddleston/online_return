from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import Character, Player

# Create your views here.

def index(request):
    return render(request, 'character/index.html')

@login_required
def player(request):
    return HttpResponse("Hello world. You're in the Character module looking at your player details.")

@login_required
def list(request):
    #Get user Player details
    current_player = Player.objects.get(user=request.user)
    characters =  Character.objects.filter(player=current_player)
    current_characters = characters.filter(state='A')
    previous_characters = characters.exclude(state='A')
    context = {'current_characters': current_characters, 'previous_characters': previous_characters}
    return render(request, 'character/list.html', context)

@login_required
def details(request, character_id):
    character = get_object_or_404(Character, pk=character_id)
    if character.player.user != request.user:
        return HttpResponse('Unauthorized', status=401)
    return render(request, 'character/details.html', {'character': character})
