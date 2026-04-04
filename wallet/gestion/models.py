from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError

# Create your models here.

# El Cliente extiende al usuario
class Cliente(models.Model):
    #name = models.CharField("Nombre", max_length=200)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dni = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Cuenta(models.Model):
    client = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='cuentas')
    account_number = models.CharField(max_length=20, unique=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    currency = models.CharField(max_length=10, default='CLP')
    status = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cuenta {self.id} - {self.client} - {self.account_number}"
    
class Transaccion(models.Model):
    TYPE_TRANSACTION = [
        ('ingreso', 'Ingreso'),
        ('egreso', 'Egreso'),
    ]

    source_account = models.ForeignKey(
        Cuenta, on_delete=models.CASCADE, related_name='transacciones_salientes'
    )
    destination_account = models.ForeignKey(
        Cuenta, on_delete=models.CASCADE, related_name='transacciones_entrantes'
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    type_trx = models.CharField(max_length=20, choices=TYPE_TRANSACTION)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pendiente')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.type_trx} - {self.amount}"
    
    def clean(self):
        if self.type_trx == 'egreso' and not (self.source_account and self.destination_account):
            raise ValidationError("Transferencia requieren cuenta origen y destino")