from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import *


def index(request):
    games = Game.objects.all()
    platforms = Platform.objects.all()
    languages = Language.objects.all()
    return render(request, 'nca/index.html', {'games': games, 'platforms': platforms, 'languages': languages})


def request_detail(request, gamer_request_id):
    game_request = get_object_or_404(GameRequest, pk=gamer_request_id)
    rating = round(
        10 * game_request.requestlikes_set.filter(liked=True).count() / game_request.requestlikes_set.count(), 2)
    return render(request, 'nca/request_detail.html', {'game_request': game_request, 'rating': rating})


def request_post(request):
    return HttpResponse("Hello, world. You're at the polls index.")
