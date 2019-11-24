from django import forms

class Addfriend(forms.Form):
	username = forms.CharField(label='username', max_length=100)

class Addexpense(forms.Form):
	paidby = forms.CharField(label='paidby',max_length=1000)
	indpaid = forms.CharField(label='indpaid',max_length=1000)
	split = forms.CharField(label='split',max_length=1000)
	indamt = forms.CharField(label='indamt',max_length=1000)
	amt =  forms.FloatField(label='amt')
	reason = forms.CharField(label='reason',max_length=1000)
