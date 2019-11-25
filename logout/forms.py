from django import forms

class Passchange(forms.Form):
    newpassword = forms.CharField( widget=forms.PasswordInput )
    confirmpassword = forms.CharField( widget=forms.PasswordInput )
