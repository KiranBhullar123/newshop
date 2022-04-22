from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import request


class RegisterForm(forms.ModelForm):
    username = forms.CharField(label="Username", max_length=100)
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username',)

    def clean_password2(self):
        pass1 = self.cleaned_data.get("password1")
        pass2 = self.cleaned_data.get("password2")
        if pass1 and pass2 and pass1 != pass2:
            raise forms.ValidationError("Password don't match")
        return pass2

    def save(self, commit=True):
        userobj = super(RegisterForm, self).save(commit=False)
        userobj.set_password(self.cleaned_data["password2"])
        userobj.is_active = True

        if commit:
            userobj.save()
        return userobj

class MyLoginForm(forms.Form):
    uname = forms.CharField(label='Username')
    pass1 = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean(self):
        username1 = self.cleaned_data.get("uname")
        password1 = self.cleaned_data.get("pass1")
        userobj = authenticate(request, username=username1, password=password1) #authenticate function
        if userobj is None:
            raise forms.ValidationError("Invalid username/password")
        return super(MyLoginForm, self).clean()