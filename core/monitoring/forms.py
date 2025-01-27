from django import forms
from .models import Asset

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ["name", "symbol", "inferior_limit", "superior_limit", "frequency"]


class PriceHistoryForm(forms.Form):
    start_date = forms.DateTimeField(required=False, label = "Start date")
    end_date = forms.DateTimeField(required=False, label = "End date")