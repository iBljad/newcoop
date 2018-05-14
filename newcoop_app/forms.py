from django import forms
from django.forms import ModelForm

from .models import RequestComment, GameRequest


class RequestCommentForm(ModelForm):
    class Meta:
        model = RequestComment
        fields = '__all__'
        exclude = ['pub_date', 'active']
        widgets = {
            'user': forms.HiddenInput,
            'request': forms.HiddenInput
        }


class RequestPostForm(ModelForm):
    class Meta:
        model = GameRequest
        fields = '__all__'
        exclude = ['pub_date', 'active', ]
        widgets = {
            'user': forms.HiddenInput,
        }


class RequestSearchForm(forms.Form):
    q = forms.CharField(label='Query', max_length=80)
