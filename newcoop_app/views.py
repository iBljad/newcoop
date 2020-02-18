from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .forms import RequestCommentForm, RequestSearchForm, RequestPostForm
from .models import *

not_authorised = 'You are not authorised, please log in'
server_error = 'Something went wrong'


def index(request):
    search_form = RequestSearchForm()
    post_form = RequestPostForm(initial={'user': request.user})
    latest_requests = GameRequest.objects.filter(active=True).order_by('-pub_date')[:5]
    return render(
        request, 'newcoop_app/index.html',
        {'search_form': search_form, 'post_form': post_form, 'latest': latest_requests}
    )


class RequestDetailsView(generic.DetailView):
    model = GameRequest
    template_name = 'newcoop_app/request_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        game_request = self.get_object()
        context['likes'] = game_request.requestlikes_set.filter(liked=True).count()
        context['comments'] = game_request.requestcomment_set.order_by('-pub_date')
        user = self.request.user

        if user.is_authenticated:
            form = RequestCommentForm(initial={'user': user, 'request': game_request})
            context['form'] = form
            context['voted'] = game_request.requestlikes_set.filter(liked=True, user=user).exists()
        return context


def request_post(request):
    if request.method == 'POST':
        post_form = RequestPostForm(request.POST)
        if post_form.is_valid() and int(post_form.data['user']) == request.user.id:
            post_form.save()
            messages.add_message(request, messages.SUCCESS, 'Request posted successfully')
        else:
            messages.add_message(request, messages.ERROR, server_error)
        return HttpResponseRedirect(reverse('newcoop_app:index'))


def like_post(request, game_request_id):
    try:
        user = request.user
        is_liked = True if request.POST['action'] == 'Like' else False
        game_request = GameRequest.objects.get(pk=game_request_id)
    except KeyError:
        messages.add_message(request, messages.ERROR, server_error)
        return HttpResponseRedirect(reverse('newcoop_app:request_detail', args=(game_request_id,)))
    else:
        if user.is_authenticated:
            RequestLikes.objects.update_or_create(user=user, request=game_request,
                                                  defaults={'liked': is_liked, 'pub_date': timezone.now()})
            messages.add_message(request, messages.SUCCESS, 'We\'ve got your like')
            return HttpResponseRedirect(reverse('newcoop_app:request_detail', args=(game_request_id,)))
        else:
            messages.add_message(request, messages.WARNING, not_authorised)
            return HttpResponseRedirect(reverse('newcoop_app:request_detail', args=(game_request_id,)))


def comment_post(request, game_request_id):
    if request.method == 'POST':
        form = RequestCommentForm(request.POST)
        if form.is_valid() and int(form.data['user']) == request.user.id:
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Comment posted successfully')
        else:
            messages.add_message(request, messages.ERROR, server_error)

    else:
        messages.add_message(request, messages.ERROR, server_error)
    return HttpResponseRedirect(reverse('newcoop_app:request_detail', args=(game_request_id,)))
