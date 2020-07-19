from django import forms

class LoginForm(forms.Form):
    login = forms.CharField()
    password = forms.CharField()

class RegistrationForm(forms.Form):
    login = forms.CharField()
    password = forms.CharField()
    confirmPassword = forms.CharField()
    email = forms.CharField()

class EditForm(forms.Form):
    nameText = forms.CharField(max_length=30)
    dataText = forms.CharField(widget=forms.Textarea)