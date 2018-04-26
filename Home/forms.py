from django import forms
from django.forms import ModelForm

from Home.models import Person, Pet


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Person
        fields = ['username', 'first_name', 'last_name', 'age', 'email', 'password']


class PetForm(ModelForm):
    class Meta:
        model = Pet
        fields = ['age', 'category', 'price', 'kind', 'state']

