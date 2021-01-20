from django import forms


class CalculatorForm(forms.Form):
    value = forms.FloatField(label='Valor logrado')
