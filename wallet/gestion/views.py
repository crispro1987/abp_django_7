from django.shortcuts import render
from .forms import UserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def home(request):
    return render(request, 'base.html')

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