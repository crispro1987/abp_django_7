from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserForm, CuentaForm, TransaccionForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Cliente, Cuenta, Transaccion
from django.views.generic import ListView, CreateView, UpdateView, DeleteView 
from django.urls import reverse_lazy
from django.db import transaction
from django.contrib import messages


# Create your views here.

@login_required
def home(request):
    cliente, _ = Cliente.objects.get_or_create(user=request.user)
    cuentas = Cuenta.objects.filter(client=cliente)

    balance = sum(c.balance for c in cuentas)

    return render(request, 'base.html', {
        'balance': balance,
        'cuentas': cuentas
    })

def login_view(request):
    if request.method == 'POST':
        form = UserForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('pagina_inicio')
            else:
                form.add_error(None, 'Usuario o contraseña incorrectos')

    else:
        form = UserForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def cuenta_list(request):
    cuentas = Cuenta.objects.filter(client__user=request.user)
    return render(request, 'account_list.html',{'cuentas':cuentas})

@login_required
def cuenta_create(request):
    if request.method == 'POST':
        form = CuentaForm(request.POST)
        if form.is_valid():
            cuenta = form.save(commit=False)
            client, _ = Cliente.objects.get_or_create(user=request.user)
            cuenta.client = client
            cuenta.save()
            return redirect('account_list')
    else:
        form = CuentaForm()
    return render(request, 'account.html', {'form':form})

@login_required
def cuenta_update(request, pk):
    cuenta = Cuenta.objects.get(pk=pk)

    if request.method == 'POST':
        form = CuentaForm(request.POST, instance=cuenta)
        if form.is_valid():
            form.save()
            return redirect('account_list')
    else:
        form = CuentaForm(instance=cuenta)
    return render(request, 'account.html',{'form':form})

@login_required
def cuenta_delete(request,pk):
    cuenta = get_object_or_404(Cuenta, pk=pk, client__user=request.user)

    if request.method == 'POST':

        if cuenta.balance > 0:
            messages.error(request, "No es posible eliminar una cuenta con saldo disponible")
            return redirect('account_list')
    
        if cuenta.transacciones_salientes.exists() or cuenta.transacciones_entrantes.exists():
            messages.error(request, "No es posible eliminar una cuenta con transacciones realizadas.")
            return redirect('account_list')
    
        cuenta.delete()
        messages.success(request, "Cuenta eliminada correctamente.")
        return redirect('account_list')
    
    return render(request, 'account_delete.html',{'cuenta':cuenta})

class CuentaDeleteView(DeleteView):
    model = Cuenta
    template_name = 'account_delete.html'
    success_url = reverse_lazy('account_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.balance > 0:
            messages.error(request, "No es posible eliminar una cuenta con saldo disponible.")
            return redirect('account_list')

        if self.object.transacciones_salientes.exists() or self.object.transacciones_entrantes.exists():
            messages.error(request, "No es posible eliminar una cuenta con transacciones realizadas.")
            return redirect('account_list')

        messages.success(request, "Cuenta eliminada correctamente.")
        return super().post(request, *args, **kwargs)

class TransaccionCreateView(CreateView):
    model = Transaccion
    form_class = TransaccionForm
    template_name = 'transaction.html'
    success_url = reverse_lazy('account_list')

    def form_valid(self, form):
        with transaction.atomic():
            transaccion = form.save(commit=False)

            origin = transaccion.source_account
            destiny = transaccion.destination_account
            amount = transaccion.amount

            # Restar a la cuenta de origen
            origin.balance -= amount
            origin.save()

            # sumar saldo a la cuenta de destino
            destiny.balance += amount
            destiny.save()

            # guardar la transaccion
            transaccion.type_trx = 'egreso'
            transaccion.save()

        messages.success(self.request, "La transferencia se ha realizado con exito.")
        return super().form_valid(form)



