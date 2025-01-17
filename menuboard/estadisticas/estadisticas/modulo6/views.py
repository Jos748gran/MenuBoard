from django.shortcuts import render

def estadistica(request):
    return render(request, 'Modulo6/estadistica.html')


def meseros(request, *args, **kwargs):
    return render(request, 'Modulo6/meseros.html')

def mesas(request, *args, **kwargs):
    return render(request, 'Modulo6/mesas.html')


def productos(request, *args, **kwargs):
    return render(request, 'Modulo6/productos.html')