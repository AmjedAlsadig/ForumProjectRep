from django import forms
from django.contrib.auth import get_user_model

class loginForm(forms.Form):
    username    =   forms.CharField(widget=forms.TextInput)  
    password    =   forms.CharField(widget=forms.PasswordInput)
User = get_user_model()
class registerForm(forms.Form):
    username    =   forms.CharField(widget=forms.TextInput)
    email       =   forms.EmailField(widget=forms.EmailInput)
    password    =   forms.CharField(widget=forms.PasswordInput)
    password2   =   forms.CharField(widget=forms.PasswordInput,label="Confirm password")

    def clean_username(self):
        username = self.cleaned_data.get("username")
        qs       = User.objects.filter(username = username)

        if qs.exists():
            raise forms.ValidationError("Username is used")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs       = User.objects.filter(email = email)

        if qs.exists():
            raise forms.ValidationError("email is used")
        return email
    def clean(self):
        data            = self.cleaned_data
        password        = self.cleaned_data.get("password")
        password2       = self.cleaned_data.get("password2")

        if password != password2 :
            raise forms.ValidationError("password does not match")
        return data