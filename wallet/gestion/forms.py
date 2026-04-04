from django import forms
from .models import Cuenta, Transaccion

class UserForm(forms.Form):
    username = forms.CharField(max_length=20, error_messages={'max_length':'nombre muy largo'},
        widget=forms.TextInput(attrs={
            'class': 'form-control mt-4',
            'placeholder': 'Nombre de usuario',
            'autocomplete': 'off'
        }))
    password = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña',
            'type': 'password',
            'autocomplete': 'off'
        }))
    
    
class CuentaForm(forms.ModelForm):
    class Meta:
        model = Cuenta
        fields = ['client','account_number','balance']
        widgets = {
            'client': forms.Select(attrs={'class': 'form-control'}),
            'account_number': forms.TextInput(attrs={'class': 'form-control'}),
            'balance': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class TransaccionForm(forms.ModelForm):
    class Meta:
        model = Transaccion
        fields = ['source_account','destination_account', 'amount', 'description']

    def clean(self):
        cleaned_data = super().clean()
        origin = cleaned_data.get("source_account")
        destiny = cleaned_data.get("destination_account")
        amount = cleaned_data.get("amount")

        if origin and destiny:
            if origin == destiny:
                raise forms.ValidationError("No puedes transferir a la misma cuenta")

            if origin.balance < amount:
                raise forms.ValidationError("Saldo insuficiente")

        return cleaned_data