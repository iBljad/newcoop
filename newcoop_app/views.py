from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import *


def index(request):
    games = Game.objects.all()
    platforms = Platform.objects.all()
    languages = Language.objects.all()
    return render(request, 'nca/index.html', {'games': games, 'platforms': platforms, 'languages': languages})


class RequestDetailsView(generic.DetailView):
    model = GameRequest
    template_name = 'nca/request_detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        game_request = self.get_object()
        context['likes'] = game_request.requestlikes_set.filter(liked=True).count()
        if self.request.user.is_authenticated:
            context['voted'] = game_request.requestlikes_set.filter(liked=True, user=self.request.user).exists()
        return context


def request_post(request):
    try:
        game = Game.objects.get(pk=request.POST['game'])
        platform = Platform.objects.get(pk=request.POST['platform'])
        language = Language.objects.get(pk=request.POST['language'])
        mic = request.POST.get('mic', False)
        comment = request.POST.get('comment', '')
        user = request.user
    except KeyError:
        messages.add_message(request, messages.ERROR, 'Something went wrong')
        return HttpResponseRedirect(reverse('newcoop_app:index'))
    else:
        if user.is_authenticated:
            game_request = GameRequest(game=game, platform=platform, language=language,
                                       mic_present=True if mic is not False else False, comment=comment,
                                       user=request.user)
            game_request.save()
            messages.add_message(request, messages.SUCCESS, 'Your request successfully created')
            return HttpResponseRedirect(reverse('newcoop_app:request_detail', args=(game_request.id,)))
        else:
            messages.add_message(request, messages.WARNING, 'You are not authenticated, please log in')
            return HttpResponseRedirect(reverse('newcoop_app:index'))


def like_post(request, game_request_id):
    try:
        user = request.user
        is_liked = True if request.POST['action'] == 'Like' else False
    except KeyError:
        messages.add_message(request, messages.ERROR, 'Something went wrong')
        return HttpResponseRedirect(reverse('newcoop_app:request_detail', args=(game_request_id,)))
    else:
        if user.is_authenticated:
            RequestLikes.objects.update_or_create(user=user, request_id=game_request_id,
                                                  defaults={'liked': is_liked, 'pub_date': timezone.now()})
            messages.add_message(request, messages.SUCCESS, 'We\'ve got your like')
            return HttpResponseRedirect(reverse('newcoop_app:request_detail', args=(game_request_id,)))
        else:
            messages.add_message(request, messages.WARNING, 'You are not authenticated, please log in')
            return HttpResponseRedirect(reverse('newcoop_app:index'))

    # return HttpResponse("Hello, world. You're at the polls index.")
