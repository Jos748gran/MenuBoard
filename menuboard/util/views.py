from django.contrib.auth import login
from pedidos.forms import CustomLoginForm, CustomUserCreationForm
from django.contrib.auth import login as auth_login, authenticate
from django.shortcuts import render, redirect
from pedidos.models import Plato, Mesa, Cliente, Pedido, Mesero, PersonalCocina
from django.contrib import messages
from django.conf import settings
from .models import UserProfile

# Create your views here.
def home(request):
    data = {
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
    }
    return render(request, 'home.html', data)
def user(request):
    data = {
    'platos': Plato.objects.all(),
    }
    return render(request, 'user.html', data)

def item_pedido_list(request):
    user = request.user
    try:
        user_profile = UserProfile.objects.get(user=user)
        cliente = Cliente.objects.get(cedula=user_profile.cedula)
        items_pedido = cliente.item_pedido_list.all()
    except (UserProfile.DoesNotExist, Cliente.DoesNotExist):
        items_pedido = []
    data = {
        'item_pedido_list': items_pedido,
    }
    return render(request, 'user/item_pedido_list.html', data)

def staff(request):
    data = {
        'meteoblue_url': settings.METEOBLUE_URL,
    }
    return render(request, 'staff.html', data)

def pedidos(request):
    user = request.user
    if user.groups.filter(name='Clientes').exists():
        user_profile = UserProfile.objects.get(user=user)
        cliente = Cliente.objects.get(cedula=user_profile.cedula)
        data = {
            'pedidos': Pedido.objects.filter(cliente=cliente),
        }
        return render(request, 'user/pedidos.html', data)
    elif user.groups.filter(name='Empleados').exists():
        data = {
            'pedidos': Pedido.objects.all(),
        }
        return render(request, 'pedidos.html', data)

def menus(request):
    data = {
        'platos': Plato.objects.all(),
    }
    return render(request, 'menus.html', data)

def mesas(request):
    data = {
        'mesas': Mesa.objects.all(),
    }
    return render(request, 'mesas.html', data)

def clientes(request):
    data = {
        'clientes': Cliente.objects.all(),
    }
    return render(request, 'clientes.html', data)

def meseros(request):
    data = {
        'meseros': Mesero.objects.all(),
    }
    return render(request, 'meseros.html', data)

def personal_cocina(request):
    data = {
        'personales_cocina': PersonalCocina.objects.all(),
    }
    return render(request, 'personal_cocina.html', data)
def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, 'Inicio de sesión exitoso')
                if user.groups.filter(name='Clientes').exists():
                    return redirect('user')
                elif user.groups.filter(name='Empleados').exists():
                    return redirect('staff')
                else:
                    messages.error(request, 'No tiene permisos asignados')
                    return redirect('login')
            else:
                messages.error(request, 'Nombre de usuario o contraseña incorrectos')
        else:
            messages.error(request, 'Información proporcionada no válida')
    else:
        form = CustomLoginForm()
    return render(request, 'login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Guarda el usuario
            login(request, user)  # Inicia sesión automáticamente
            messages.success(request, 'Usuario registrado exitosamente')
            return redirect('user')  # Redirige a la página de usuario
        else:
            messages.error(request, 'Error en el registro. Verifica los datos.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})