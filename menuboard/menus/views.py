from itertools import product

from django.shortcuts import render
from menus.models import Producto, Categoria


# Create your views here.
def index(request):
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()
    return render(request, 'index.html',
                  context={'p': productos, 'c': categorias})
