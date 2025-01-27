from django import forms
from .models import Asset

class AssetForm(forms.ModelForm):
    # Form related to Asset model, used to register/edit Assets
    class Meta:
        model = Asset
        fields = ["name", "symbol", "inferior_limit", "superior_limit", "frequency"]


class PriceHistoryFilterForm(forms.Form):
    # Form for filtering price history data
    start_date = forms.DateTimeField(required=False, label = "Start date")
    end_date = forms.DateTimeField(required=False, label = "End date")