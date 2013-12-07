# coding: utf-8

__author__ = 'tomek'

from django.forms import ModelForm, Form, CharField, EmailField, PasswordInput
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class LoginForm(ModelForm):
    class Meta:
        model = User


class RegisterForm(Form):
    login = CharField()
    email = EmailField()
    password = CharField(widget=PasswordInput, label="Password")
    rpassword = CharField(widget=PasswordInput, label="Repeat password")
    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        if (cleaned_data.get('password') !=
            cleaned_data.get('rpassword')):
            raise ValidationError(u"Podane hasła nie pasują :(")
        if len(User.objects.filter(username=cleaned_data.get('login')))>0:
            raise ValidationError(u"Użytkownik o podanym loginie istnieje :(")
        return cleaned_data
