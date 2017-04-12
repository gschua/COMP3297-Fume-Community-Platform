from django import forms
from django.forms import ModelForm
from fume.models import Transaction, Platform, Tag

class AddToCartForm(forms.ModelForm):
	platform = forms.ModelChoiceField(queryset=Platform.objects.all(), widget=forms.RadioSelect, to_field_name="text")
	class Meta:
		model = Transaction
		fields = [ 'platform' ]

class NewTagForm(forms.ModelForm):
	text = forms.CharField(label='Add Tag')
	class Meta:
		model = Tag
		fields = [ 'text' ]
