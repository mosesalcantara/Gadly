from django import forms
from django.core.exceptions import ValidationError

class TextForm(forms.Form):
    input_text = forms.CharField(max_length=300)


