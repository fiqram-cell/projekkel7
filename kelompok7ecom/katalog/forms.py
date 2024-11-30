# forms.py
from django import forms

class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Alamat Pengiriman'}),
        label='Alamat Pengiriman'
    )
    phone_number = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'placeholder': 'Nomor Telepon'}),
        label='Nomor Telepon'
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'placeholder': 'Catatan (opsional)', 'rows': 3}),
        label='Catatan'
    )
