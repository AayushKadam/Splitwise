from django import forms

class UserForm(forms.Form):
    username = forms.CharField(label='username', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class NewUserForm(forms.Form):
    username = forms.CharField(label='username', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(label='email')
    phone = forms.CharField(label='phone',max_length=10)
    first_name = forms.CharField(label='first_name', max_length=100)
    last_name = forms.CharField(label='last_name', max_length=100)
