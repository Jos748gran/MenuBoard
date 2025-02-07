from django.shortcuts import render
from .models import Mesero
from .models import Mesa
from .models import  Item_Factura
import matplotlib.pyplot as plt
from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Reporte

def estadistica(request):
    return render(request, 'Modulo6/estadistica.html')

def meseros(request):
    meseros = Mesero.objects.all()
    return render(request, 'Modulo6/meseros.html', {'mesero': meseros})


def grafico_pastel(request):
    # Obtener los datos de la base de datos
    meseros = Mesero.objects.all()

    # Extraer nombres y pedidos en listas
    nombres = [mesero.nombre for mesero in meseros]
    pedidos = [mesero.pedidosAtendidos for mesero in meseros]

    # Crear el gráfico
    plt.figure(figsize=(6, 6))  # Tamaño del gráfico
    plt.pie(pedidos, labels=nombres, autopct='%1.1f%%', startangle=90)
    plt.title("Pedidos por Mesero")

    # Guardar el gráfico en un buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Retornar el gráfico como una respuesta HTTP
    return HttpResponse(buffer, content_type='image/png')

def mesas(request):
    mesas = Mesa.objects.all()
    return render(request, 'Modulo6/mesas.html', {'mesas': mesas})

def grafico_mesa(request):
    # Obtener los datos de la base de datos
    mesas = Mesa.objects.all()

    # Extraer cantidad de uso y códigos de las mesas
    cantidad_usos = [mesa.cantidad_uso for mesa in mesas]
    codigos = [mesa.codigo for mesa in mesas]

    # Crear el gráfico
    plt.figure(figsize=(6, 6))  # Tamaño del gráfico
    plt.pie(cantidad_usos, labels=codigos, autopct='%1.1f%%', startangle=90)
    plt.title("Pedidos por Mesa")

    # Guardar el gráfico en un buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Retornar el gráfico como una respuesta HTTP
    return HttpResponse(buffer, content_type='image/png')

def productos(request):
    productos = Item_Factura.objects.all()
    return render(request, 'Modulo6/productos.html', {'productos': productos})

def grafico_producto(request):
    # Obtener los datos de la base de datos
    items_factura = Item_Factura.objects.all()

    # Extraer nombres y cantidades en listas
    nombres = [item.producto.nombre for item in items_factura]
    cantidades = [item.cantidad for item in items_factura]

    # Crear el gráfico
    plt.figure(figsize=(6, 6))  # Tamaño del gráfico
    plt.pie(cantidades, labels=nombres, autopct='%1.1f%%', startangle=90)
    plt.title("Productos más vendidos")

    # Guardar el gráfico en un buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Retornar el gráfico como una respuesta HTTP
    return HttpResponse(buffer, content_type='image/png')



