from django import forms
from .models import Cuenta, Transaccion, User
from django.contrib.auth.forms import UserCreationForm

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
    

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Correo electrónico'
        })
        )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control'
            })
            
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Nombre de usuario'
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Contraseña'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Repetir contraseña'
        })
    
    
class CuentaForm(forms.ModelForm):
    class Meta:
        model = Cuenta
        fields = ['account_type','account_number']
        widgets = {
            'account_type': forms.Select(attrs={'class': 'form-control'}),
            'account_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

class TransaccionForm(forms.ModelForm):
    class Meta:
        model = Transaccion
        fields = ['source_account','destination_account', 'amount', 'description']
        widgets = {
            'source_account': forms.Select(attrs={'class': 'form-control'}),
            'destination_account': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }

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