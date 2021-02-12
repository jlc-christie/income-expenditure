from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import IEStatement, Person, Address


class PersonForm(UserCreationForm):
    date_of_birth = forms.DateField()
    phone_number = forms.CharField(max_length=11)
    paon = forms.CharField(max_length=80, required=True)
    saon = forms.CharField(max_length=80, required=False)
    street = forms.CharField(max_length=80, required=True)
    town_city = forms.CharField(max_length=80, required=True)
    county = forms.CharField(max_length=80, required=True)
    postcode = forms.CharField(max_length=8, required=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

    def save(self, commit=True):
        user = super(PersonForm, self).save(commit=False)
        user.username = user.email
        user.save()
        address = Address(
            paon=self.cleaned_data['paon'],
            saon=self.cleaned_data['saon'],
            street=self.cleaned_data['street'],
            town_city=self.cleaned_data['town_city'],
            county=self.cleaned_data['county'],
            postcode=self.cleaned_data['postcode']
        )
        address.save()
        person = Person(user=user, address=address)
        person.save()
        return person


class IEStatementForm(ModelForm):
    class Meta:
        model = IEStatement
        fields = ['salary', 'income_other', 'mortgage', 'rent', 'utilities', 'travel', 'food', 'loans',
                  'credit_cards', 'expenditure_other']

