from django.contrib import admin
from .models import Cliente, Cuenta, Transaccion

# Register your models here.

admin.site.register(Cliente)
admin.site.register(Cuenta)
admin.site.register(Transaccion)


