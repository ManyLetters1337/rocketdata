from django import forms


class CityNameFilterForm(forms.Form):
    """
    City Filter Form
    """
    name = forms.CharField(max_length=50)
