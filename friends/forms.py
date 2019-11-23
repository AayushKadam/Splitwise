from django import forms

class Addfriend(forms.Form):
	username = forms.CharField(label='username', max_length=100)
