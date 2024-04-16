from .models import Bids
from django import forms
from django.db.models import Max


class Close_Bid_form(forms.Form):
    owner = forms.ModelChoiceField()

