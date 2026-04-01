from django import forms

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