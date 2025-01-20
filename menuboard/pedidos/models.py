from enum import Enum

from django.core.validators import MinValueValidator
from django.db import models
from abc import ABC, abstractmethod, ABCMeta
from django.db.models.base import ModelBase


#Enumerador:
class Estado(Enum):
    en_preparacion = 'EN_PREPARACION'
    pagado = 'PAGADO'
    pendiente = 'PENDIENTE'
    preparado = 'PREPARADO'
    servido = 'SERVIDO'
    reservado = 'RESERVADO'

#Interfazes:
class MultiModelABCMeta(ModelBase, ABCMeta):
    pass
class InteraccionPedido(models.Model, ABC, metaclass=MultiModelABCMeta):
    class Meta:
        abstract = True
    #Metodos:
    @abstractmethod
    def actualizar_estado(self, estado:'Estado', pedido:'Pedido'):
        pass
    @abstractmethod
    def visualizar_estado(self, pedido:'Pedido'):
        pass

class InteraccionCliente(models.Model):
    class Meta:
        abstract = True
    #Metodos:
    @abstractmethod
    def agregar_cliente(self):
        pass
    @abstractmethod
    def anotar_pedido(self, pedido:'Pedido'):
        pass
    @abstractmethod
    def asignar_mesa(self):
        pass
    @abstractmethod
    def atender_pedido(self):
        pass
    @abstractmethod
    def gestionar_pedido(self):
        pass
    @abstractmethod
    def mostrar_cuenta(self):
        pass
    @abstractmethod
    def mostrar_menu(self):
        pass
    @abstractmethod
    def realizar_reserva(self):
        pass
#Clases:
class Persona(models.Model):
    #Atributos:
    cedula = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=50)
    telefono = models.CharField(max_length=10, unique=True)
    class Meta:
        abstract = True

class Empleado(Persona, InteraccionPedido):
    #Atributos:
    identificacion = models.CharField(max_length=7, unique=True, null=True, editable=False)
    #Asociacion:
    pedidos = models.ManyToManyField('Pedido', blank=True, editable=False)
    class Meta:
        abstract = True
    #Metodos:
    def actualizar_estado(self, estado:Estado, pedido:'Pedido'):
        pedido.estado = estado
    def visualizar_estado(self, pedido:'Pedido'):
        return pedido.estado

class Mesero(Empleado):
    #Atributos
    esta_ocupado = models.BooleanField(default=False, editable=False)
    class Meta:
        verbose_name = "Mesero"
        verbose_name_plural = "Meseros"
    #Metodos:
    def save(self, *args, **kwargs):
        if not self.identificacion:
            letra_nombre = self.nombre[0].upper()
            empleados = Mesero.objects.filter(identificacion__startswith=f"11M").count() + 1
            self.identificacion = f"11M{letra_nombre}{empleados:02d}"
        super().save(*args, **kwargs)
    def entregar_pedido(self, pedido:'Pedido'):
        super().actualizar_estado(Estado.servido, pedido)
    def __str__(self):
        return self.nombre+' | '+self.identificacion

class PersonalCocina(Empleado):
    #Atributos:
    esta_cocinando = models.BooleanField(default=False, editable=False)
    class Meta:
        verbose_name = "Personal de Cocina"
        verbose_name_plural = "Personales de Cocina"
    #Metodos:
    def save(self, *args, **kwargs):
        if not self.identificacion:
            letra_nombre = self.nombre[0].upper()
            empleados = PersonalCocina.objects.filter(identificacion__startswith=f"11P").count() + 1
            self.identificacion = f"11P{letra_nombre}{empleados:02d}"
        super().save(*args, **kwargs)
    def preparar_pedido(self):
        pass
    def servir_pedido(self):
        pass
    def __str__(self):
        return self.nombre+' | '+self.identificacion

class Cliente(Persona):
    #Atributos:
    cantidad_persona = models.PositiveIntegerField(editable=False, default=1)
    es_para_llevar = models.BooleanField(editable=False, default=False)
    realizo_pedido = models.BooleanField(editable=False,default=False)
    #Asociacion:
    historial = models.OneToOneField('Historial', on_delete=models.CASCADE, null=True, editable=False,
                                     related_name='cliente')
    mesa = models.OneToOneField('Mesa', on_delete=models.CASCADE, null=True, editable=False)
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
    #Metodos:
    def save(self, *args, **kwargs):
        if not self.historial:
            historial = Historial.objects.create()
            self.historial = historial
        super().save(*args, **kwargs)
    def modificar_pedido(self):
        pass
    def ocupar_mesa(self, mesa_ocupada):
        self.mesa = mesa_ocupada
    def realizar_pago(self):
        pass
    def realizar_pedido(self):
        pass
    def visualizar_mesa_asignada(self):
        pass

    def __str__(self):
        return self.nombre+' | '+self.cedula

class ItemPedido(models.Model):
    #Atributos:
    cantidad = models.PositiveIntegerField(default=1)
    observacion = models.CharField(max_length=100 ,blank=True, default='Ninguna')
    #Asociacion:
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='item_pedido_list')
    plato = models.OneToOneField('Plato', on_delete=models.CASCADE)
    class Meta:
        verbose_name = "Item del Pedido"
        verbose_name_plural = "Items del Pedido"
    # Metodos:
    def __str__(self):
        return self.plato.nombre+' | '+str(self.cantidad)+' | '+self.cliente.nombre+' | '+self.observacion

class Pedido(models.Model):
    #Atributos:
    fecha_actual = models.DateTimeField(auto_now=True, editable=False)
    informacion = models.TextField(editable=False)
    numero = models.PositiveIntegerField(editable=False, unique=True)
    cliente = models.OneToOneField('Cliente', on_delete=models.CASCADE)
    #Asociacion:
    estado = models.CharField(max_length=50, choices=[(tag.value, tag.name) for tag in Estado], default=Estado.pendiente)
    mesa = models.OneToOneField('Mesa', on_delete=models.CASCADE, null=True, blank=True)
    item_pedido_list = models.ManyToManyField(ItemPedido, blank=True)
    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
    #Metodos:
    def save(self, *args, **kwargs):
        if not self.numero:
            self.numero = Pedido.objects.count() + 1
        super().save(*args, **kwargs)
    def agregar_item(self):
        pass
    def calcular_total(self):
        pass
    def mostrar_tiempo_espera(self):
        pass
    def registrar_informacion(self):
        pass
    def remover_item(self):
        pass
    def __str__(self):
        return str(self.numero)+' | '+str(self.fecha_actual)+' | '+str(self.estado)+' | '+str(self.mesa.numero)

class Historial(models.Model):
    #Atributos:
    pedidos = models.ManyToManyField(Pedido)
    class Meta:
        verbose_name = "Historial"
        verbose_name_plural = "Historiales"
    #Metodos:
    def agregar_pedido(self):
        pass
    def mostrar_informacion(self):
        pass
    def __str__(self):
        return str(self.id)+' | '+self.cliente.nombre

class Restaurante(InteraccionCliente):
    #Atributos:
    nombre = models.CharField(max_length=50)
    #Asociacion:
    clientes = models.ManyToManyField(Cliente, blank=True)
    meseros = models.ManyToManyField(Mesero, blank=True)
    personal_cocina_list = models.ManyToManyField(PersonalCocina, blank=True)
    pedidos = models.ManyToManyField(Pedido, blank=True)
    mesas = models.ManyToManyField('Mesa', blank=True)
    menu = models.OneToOneField('Menu', on_delete=models.CASCADE, null=True, blank=True)
    registro_historico = models.OneToOneField('RegistroHistorico', on_delete=models.CASCADE, null=True,
                                              editable=False, related_name='restaurante')
    class Meta:
        verbose_name = "Restaurante"
        verbose_name_plural = "Restaurantes"
    #Metodos:
    def save(self, *args, **kwargs):
        if not self.registro_historico:
            registro = RegistroHistorico.objects.create()
            self.registro_historico = registro
        super().save(*args, **kwargs)
    def agregar_cliente(self):
        pass
    def agregar_mesero(self):
        pass
    def agregar_personal_cocina(self):
        pass
    def mostrar_historial(self):
        pass
    def mostrar_mesas_disponibles(self):
        pass
    def mostrar_registro_historico(self):
        pass
    def remover_mesa(self):
        pass
    def __str__(self):
        return self.nombre
    #Interfaz:
    def agregar_cliente(self):
        pass
    def anotar_pedido(self, pedido: 'Pedido'):
        pass
    def asignar_mesa(self):
        pass
    def atender_pedido(self):
        pass
    def gestionar_pedido(self):
        pass
    def mostrar_cuenta(self):
        pass
    def mostrar_menu(self):
        pass
    def realizar_reserva(self):
        pass

class Plato(models.Model):
    #Atributos:
    nombre = models.CharField(max_length=50, unique=True)
    precio = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])
    class Meta:
        verbose_name = "Plato"
        verbose_name_plural = "Platos"
    #Metodos:
    def __str__(self):
        return self.nombre+' | '+str(self.precio)


class Menu(models.Model):
    #Asociacion:
    platos = models.ManyToManyField(Plato)
    class Meta:
        verbose_name = "Menu"
        verbose_name_plural = "Menus"
    #Metodos:
    def agregar_plato(self):
        pass
    def mostrar_platos(self):
        pass
    def remover_plato(self):
        pass
    def __str__(self):
        return str(self.id)

class Mesa(models.Model):
    #Atributos:
    capacidad = models.PositiveIntegerField(default=1)
    esta_disponible = models.BooleanField(default=True, editable=False)
    numero = models.PositiveIntegerField(editable=False, unique=True)
    class Meta:
        verbose_name = "Mesa"
        verbose_name_plural = "Mesas"
    #Metodos:
    def save(self, *args, **kwargs):
        if not self.numero:
            self.numero = Mesa.objects.count() + 1
        super().save(*args, **kwargs)
    def desocupar(self):
        self.esta_disponible = True
    def reservar(self):
        self.esta_disponible = False
    def __str__(self):
        return str(self.numero)+' | '+str(self.capacidad)+' | '+str(self.esta_disponible)

class RegistroHistorico(models.Model):
    pedidos = models.ManyToManyField(Pedido, editable=False, blank=True)
    #Metodos:
    def registrar_pedido(self):
        pass
    def mostrar_lista_pedidos(self):
        pass
    def __str__(self):
        return str(self.id)+' | '+self.restaurante.nombre