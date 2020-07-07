from django import forms
from django.forms import HiddenInput

from .models import Suggestion, Account, APISearch
from .models import Suggestion, Account, Order, ProfilePic


class ProfilePicForm(forms.ModelForm):
    class Meta:
        model = ProfilePic
        fields = ('pic', )

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        widgets = {'order_id': HiddenInput(),
                   'driver_id': HiddenInput(),
                   'item_list': HiddenInput()}
        fields = ('notes',
                  'delivery_address_PartA',
                  'delivery_address_PartB',
                  'delivery_address_City',
                  'delivery_address_State',
                  'delivery_address_ZIP',
                  'order_id',
                  'driver_id',
                  'item_list')


class SuggestionFormForm(forms.ModelForm):

    class Meta:
        model = Suggestion
        fields = ('Title', 'Text')


class APITestForm(forms.ModelForm):

    class Meta:
        model = APISearch
        fields = ('ItemName',)


class AccountCreationForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ('account_first_name', 'account_last_name', 'account_phone_number',
                  'account_email')
