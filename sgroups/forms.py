from django import forms

class Addgroup(forms.Form):
    group_name = forms.CharField(label='group_name', max_length=100)
    users = forms.CharField(label='users', max_length=1000)
