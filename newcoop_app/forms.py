from django import forms
from django.forms import ModelForm
from django_select2.forms import (
    ModelSelect2Widget
)

from .models import RequestComment, GameRequest, Game, Platform


class DelayedModelSelect2Widget(ModelSelect2Widget):
    def build_attrs(self, *args, **kwargs):
        attrs = super().build_attrs(*args, **kwargs)
        attrs.setdefault('data-ajax--delay', 200)
        attrs.setdefault('data-minimum-input-length', 3)
        return attrs


class RequestCommentForm(ModelForm):
    class Meta:
        model = RequestComment
        fields = '__all__'
        exclude = ['pub_date', 'active']
        labels = {
            'comment': ''
        }
        widgets = {
            'user': forms.HiddenInput,
            'request': forms.HiddenInput,
        }


class RequestPostForm(ModelForm):
    class Meta:
        model = GameRequest
        fields = '__all__'
        exclude = ['pub_date', 'active', ]
        widgets = {
            'user': forms.HiddenInput,
            'game': DelayedModelSelect2Widget(
                model=Game,
                queryset=Game.objects.all(),
                search_fields=['game_name__icontains'],
                dependent_fields={'platform': 'link__platform_id__exact'},
            ),
            'platform': DelayedModelSelect2Widget(
                model=Platform,
                # queryset=Link.objects.all(),
                search_fields=['platform_name__icontains'],
                dependent_fields={'game': 'link__game_id__exact'},
            )
        }


class RequestSearchForm(forms.Form):
    q = forms.CharField(label='', max_length=80, required=False,
                        widget=forms.TextInput(attrs={'placeholder': 'Search for requests'}))


class SelectForm(forms.Form):
    country = forms.ModelChoiceField(
        queryset=Game.objects.all(),
        label='',
        widget=ModelSelect2Widget(
            search_fields=['game_name__icontains'],
            queryset=Game.objects.all(),
        )
    )
