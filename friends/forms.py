from django import forms

class Addfriend(forms.Form):
	username = forms.CharField(label='username', max_length=100)

class Addexpense(forms.Form):
	paidby = forms.CharField(label='paidby',max_length=1000)
	split = forms.CharField(label='split',max_length=1000)
	amt =  forms.DecimalField(label='amt',decimal_places=2,max_digits=19)
	reason = forms.CharField(label='reason',max_length=1000)
