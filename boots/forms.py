
from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Wallet, WithdrawalRequests, Deposits
from .constants import coin_types

default_input_class = {'class': 'form-control'}
# dropdown = forms.DecimalInput(attrs=default_input_class)
decimal_input = forms.NumberInput(attrs=default_input_class)
text_input = forms.TextInput(attrs=default_input_class)
email_input = forms.EmailInput(attrs=default_input_class)
pwd_input = forms.PasswordInput(attrs=default_input_class)

class AuthForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100, required=True,
        widget=text_input)
    password = forms.CharField(label='Password', max_length=100, required=True,
        widget=pwd_input)

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ('eth_address', 'btc_address')
        labels = {
            'eth_address': _('Ethereum Wallet Address'),
            'btc_address': _('Bitcoin Wallet Address'),
        }
        widgets = {
            'eth_address': text_input,
            'btc_address': text_input,
        }

class WithdrawForm(forms.ModelForm):
    class Meta:
        model = WithdrawalRequests
        fields = ('amount', 'coin_type', 'address')
        labels = {
            'amount': _('Amount'),
            'coin_type': _('Address Type'),
            'address': _('Address'),
        }
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 
                'v-model': 'amount'}),
            'coin_type': forms.Select(attrs={'class': 'form-control', 
                'v-model': 'coin_type', '@change': 'change_address'}, 
                choices=((coin_types['btc'], 'Bitcoin'),(coin_types['eth'], 'Ethereum'))),
            'address': forms.TextInput(attrs={'class': 'form-control', 'v-model': 'address'}),
        }
        help_texts = {
            'address': _('Make sure the address matches the address type above to avoid coin loss'),
        }

class InvestForm(forms.ModelForm):
    class Meta:
        model = Deposits
        fields = ('coin_type', 'amount', 'sender_address', 'recipient_address')
        labels = {
            'amount': _('Amount'),
            'coin_type': _('Address Type'),
            'recipient_address': _('Platform Address'), #Platform Address
            'sender_address': _('Your Address'),
        }
        widgets = {
            'amount': decimal_input,
            'coin_type': forms.Select(attrs={'class': 'form-control', 
                'v-model': 'coin_type', '@change': 'change_address'}, choices=((coin_types['btc'], 'Bitcoin'),(coin_types['eth'], 'Ethereum'))),
            'recipient_address': forms.HiddenInput(attrs={'class': 'form-control', 'v-model': 'recipient_address'}),
            'sender_address': forms.TextInput(attrs={'class': 'form-control', 'v-model': 'sender_address'}),
        }
        help_texts = {
            # 'address': _('Make sure the address matches the address type above to avoid coin loss'),
        }
