from django.contrib.auth import login


from pedidos.models import Mesa, Cliente, Pedido, Mesero, PersonalCocina, ItemPedido
from pedidos.forms import MesaForm, ClienteForm, PedidoForm, MeseroForm, \
    PersonalCocinaForm, ItemPedidoForm, ItemPedidoFormMod, OrdenarPedidoForm
from django.contrib.auth import login as auth_login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PlatoForm
from django.contrib import messages
from util.models import UserProfile

from .models import Plato

def crear_plato(request):
    if request.method == 'POST':
        form = PlatoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Plato creado exitosamente')
            return redirect('menus')
    else:
        form = PlatoForm()
    return render(request, 'objetos_platos/crear_plato.html', {'form': form})

def modificar_plato(request, id):
    plato = get_object_or_404(Plato, id=id)
    if request.method == "POST":
        form = PlatoForm(request.POST, request.FILES, instance=plato)
        if form.is_valid():
            form.save()
            messages.success(request, 'Plato modificado exitosamente')
            return redirect('menus')
    else:
        form = PlatoForm(instance=plato)
    return render(request, 'objetos_platos/modificar_plato.html', {'form': form})

def eliminar_plato(request, id):
    plato = get_object_or_404(Plato, id=id)
    if request.method == "POST":
        plato.delete()
        messages.success(request, 'Plato eliminado exitosamente')
        return redirect('menus')
    return render(request, 'objetos_platos/eliminar_plato.html', {'plato': plato})

def crear_mesa(request):
    if request.method == 'POST':
        form = MesaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mesas')
    else:
        form = MesaForm()
    return render(request, 'objetos_mesas/crear_mesa.html', {'form': form})

def modificar_mesa(request, id):
    mesa = get_object_or_404(Mesa, id=id)
    if request.method == 'POST':
        form = MesaForm(request.POST, instance=mesa)
        if form.is_valid():
            form.save()
            return redirect('mesas')
    else:
        form = MesaForm(instance=mesa)
    return render(request, 'objetos_mesas/modificar_mesa.html', {'form': form})

def eliminar_mesa(request, id):
    mesa = get_object_or_404(Mesa, id=id)
    if request.method == 'POST':
        mesa.delete()
        return redirect('mesas')
    return render(request, 'objetos_mesas/eliminar_mesa.html', {'mesa': mesa})

def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clientes')
    else:
        form = ClienteForm()
    return render(request, 'objetos_clientes/crear_cliente.html', {'form': form})

def modificar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'objetos_clientes/modificar_cliente.html', {'form': form})

def eliminar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        cliente.delete()
        return redirect('clientes')
    return render(request, 'objetos_clientes/eliminar_cliente.html', {'cliente': cliente})

def crear_pedido(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pedidos')
    else:
        form = PedidoForm()
    return render(request, 'objetos_pedidos/crear_pedido.html', {'form': form})

def modificar_pedido(request, id):
    pedido = get_object_or_404(Pedido, id=id)
    if request.method == 'POST':
        form = PedidoForm(request.POST, instance=pedido)
        if form.is_valid():
            form.save()
            return redirect('pedidos')
    else:
        form = PedidoForm(instance=pedido)
        user = request.user
        if user.groups.filter(name='Clientes').exists():
            return render(request, 'user/modificar_pedido.html', {'form': form})
        elif user.groups.filter(name='Empleados').exists():
            return render(request, 'objetos_pedidos/modificar_pedido.html', {'form': form})

def eliminar_pedido(request, id):
    pedido = get_object_or_404(Pedido, id=id)
    if request.method == 'POST':
        pedido.delete()
        return redirect('pedidos')
    return render(request, 'objetos_pedidos/eliminar_pedido.html', {'pedido': pedido})

def crear_mesero(request):
    if request.method == 'POST':
        form = MeseroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('meseros')
    else:
        form = MeseroForm()
    return render(request, 'objetos_meseros/crear_mesero.html', {'form': form})

def modificar_mesero(request, id):
    mesero = get_object_or_404(Mesero, id=id)
    if request.method == 'POST':
        form = MeseroForm(request.POST, instance=mesero)
        if form.is_valid():
            form.save()
            return redirect('meseros')
    else:
        form = MeseroForm(instance=mesero)
    return render(request, 'objetos_meseros/modificar_mesero.html', {'form': form})


def eliminar_mesero(request, id):
    mesero = get_object_or_404(Mesero, id=id)
    if request.method == 'POST':
        mesero.delete()
        return redirect('meseros')
    return render(request, 'objetos_meseros/eliminar_mesero.html', {'mesero': mesero})

def crear_personal_cocina(request):
    if request.method == 'POST':
        form = PersonalCocinaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('personal_cocina')
    else:
        form = PersonalCocinaForm()
    return render(request, 'objetos_personal_cocina/crear_personal_cocina.html', {'form': form})

def modificar_personal_cocina(request, id):
    personal_cocina = get_object_or_404(PersonalCocina, id=id)
    if request.method == 'POST':
        form = PersonalCocinaForm(request.POST, instance=personal_cocina)
        if form.is_valid():
            form.save()
            return redirect('personal_cocina')
    else:
        form = PersonalCocinaForm(instance=personal_cocina)
    return render(request, 'objetos_personal_cocina/modificar_personal_cocina.html', {'form': form})

def eliminar_personal_cocina(request, id):
    personal_cocina = get_object_or_404(PersonalCocina, id=id)
    if request.method == 'POST':
        personal_cocina.delete()
        return redirect('personal_cocina')
    return render(request, 'objetos_personal_cocina/eliminar_personal_cocina.html', {'personal_cocina': personal_cocina})

def crear_item_pedido(request):
    if request.method == 'POST':
        form = ItemPedidoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pedidos')
    else:
        form = ItemPedidoForm()
    data = {
        'form': form,
    }
    return render(request, 'objetos_pedidos/crear_item_pedido.html', data)

def crear_item_pedido_user(request, id):
    user_profile = UserProfile.objects.get(user=request.user)
    plato = Plato.objects.get(id=id)
    if request.method == 'POST':
        form = ItemPedidoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('item_pedido_list')
    else:
        form = ItemPedidoForm()
    data = {
        'form': form,
        'user': request.user,
        'cliente': Cliente.objects.get(cedula=user_profile.cedula),
        'plato': plato,
    }
    return render(request, 'user/objetos_item_pedido/crear_item_pedido.html', data)

def modificar_item_pedido(request, id):
    item_pedido = get_object_or_404(ItemPedido, id=id)
    if request.method == 'POST':
        form = ItemPedidoFormMod(request.POST, instance=item_pedido)
        if form.is_valid():
            form.save()
            return redirect('item_pedido_list')
    else:
        form = ItemPedidoFormMod(instance=item_pedido)

    return render(request, 'user/objetos_item_pedido/modificar_item_pedido.html', {'form': form})

def eliminar_item_pedido(request, id):
    item_pedido = get_object_or_404(ItemPedido, id=id)
    if request.method == 'POST':
        item_pedido.delete()
        return redirect('item_pedido_list')
    return render(request, 'user/objetos_item_pedido/eliminar_item_pedido.html', {'item_pedido': item_pedido})

def ordenar_pedido(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    cliente = Cliente.objects.get(cedula=user_profile.cedula)
    if request.method == 'POST':
        form = OrdenarPedidoForm(request.POST)
        if form.is_valid():
            es_para_llevar = form.cleaned_data['es_para_llevar']
            mesa_ocupada = form.cleaned_data['mesa_ocupada']
            cliente.ordenar_pedido(es_para_llevar, mesa_ocupada)
            return redirect('pedidos')
    else:
        form = OrdenarPedidoForm()
    return render(request, 'metodos/user/ordenar_pedido.html', {'form': form, 'cliente': cliente})