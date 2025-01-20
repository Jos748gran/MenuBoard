from django.db import models
from abc import ABC, abstractmethod
from typing import List, Dict, Any


class Menu(models.Model):
    nombre = models.CharField(max_length=50)
    estado = models.BooleanField()

    def __str__(self):
        return self.nombre

    def activar_menu(self) -> None:
        self.estado = True
        self.save()

    def desactivar_menu(self) -> None:
        self.estado = False
        self.save()


class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='categorias')

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    precio = models.FloatField()
    disponibilidad = models.BooleanField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')

    def __str__(self):
        return self.nombre

    def cambiar_disponibilidad(self, disponible: bool) -> None:
        self.disponibilidad = disponible
        self.save()


# Interfaz IMenu
class IMenu(ABC):

    @abstractmethod
    def agregar_producto(self, id_categoria: int, producto: Producto) -> None:
        pass

    @abstractmethod
    def eliminar_producto(self, id_categoria: int, id_producto: int) -> None:
        pass

    @abstractmethod
    def agregar_categoria(self, menu_id: int, categoria: Categoria) -> None:
        pass

    @abstractmethod
    def eliminar_categoria(self, id_categoria: int) -> None:
        pass

    @abstractmethod
    def modificar_categoria(self, categoria: Categoria) -> None:
        pass

    @abstractmethod
    def modificar_producto(self, producto: Producto) -> None:
        pass

    @abstractmethod
    def buscar_categoria(self, nombre: str) -> List[Categoria]:
        pass

    @abstractmethod
    def buscar_producto(self, nombre: str) -> List[Producto]:
        pass

    @abstractmethod
    def mostrar_menu(self, menu_id: int) -> Dict[str, Any]:
        pass


# Implementación de IMenu
class MenuService(IMenu):

    def agregar_producto(self, id_categoria: int, producto: Producto) -> None:
        categoria = Categoria.objects.get(id=id_categoria)
        producto.categoria = categoria
        producto.save()

    def eliminar_producto(self, id_categoria: int, id_producto: int) -> None:
        Categoria.objects.get(id=id_categoria).productos.filter(id=id_producto).delete()

    def agregar_categoria(self, menu_id: int, categoria: Categoria) -> None:
        menu = Menu.objects.get(id=menu_id)
        categoria.menu = menu
        categoria.save()

    def eliminar_categoria(self, id_categoria: int) -> None:
        Categoria.objects.filter(id=id_categoria).delete()

    def modificar_categoria(self, categoria: Categoria) -> None:
        Categoria.objects.filter(id=categoria.id).update(nombre=categoria.nombre)

    def modificar_producto(self, producto: Producto) -> None:
        Producto.objects.filter(id=producto.id).update(
            nombre=producto.nombre,
            descripcion=producto.descripcion,
            precio=producto.precio,
            disponibilidad=producto.disponibilidad
        )

    def buscar_categoria(self, nombre: str) -> List[Categoria]:
        return list(Categoria.objects.filter(nombre__icontains=nombre))

    def buscar_producto(self, nombre: str) -> List[Producto]:
        return list(Producto.objects.filter(nombre__icontains=nombre))

    def mostrar_menu(self, menu_id: int) -> Dict[str, Any]:
        menu = Menu.objects.get(id=menu_id)
        return {
            "menu": menu,
            "categorias": list(menu.categorias.all())
        }
