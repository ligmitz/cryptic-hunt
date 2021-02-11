from django import forms

# Import models

from .models import Level

class LevelForm(forms.Form):
	answer = forms.CharField(label="Answer")