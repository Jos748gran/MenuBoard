from datetime import datetime
from enum import Enum
from django.core.validators import MinValueValidator
from django.db import models
import random

#Enumerador:
class Estado(Enum):
    en_preparacion = 'EN PREPARACION'
    pagado = 'PAGADO'
    pendiente = 'PENDIENTE'
    preparado = 'PREPARADO'
    servido = 'SERVIDO'
    reservado = 'RESERVADO'

#Interfaz:
class InteraccionPedido(models.Model):
    class Meta:
        abstract = True
    #Metodos:
    def actualizar_estado(self, estado:'Estado', pedido:'Pedido'):
        pass
    def visualizar_estado(self, pedido:'Pedido'):
        pass

class InteraccionCliente(models.Model):
    class Meta:
        abstract = True
    #Metodos:
    def asignar_mesa(self, cliente:'Cliente' , cantidad_persona: int):
        pass
    def atender_pedido(self):
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
        pedido.save()
    def visualizar_estado(self, pedido:'Pedido'):
        return pedido.estado

class Mesero(Empleado):
    #Atributos
    esta_ocupado = models.BooleanField(default=False, editable=False)
    #Asociacion:
    restaurante = models.ForeignKey('Restaurante', on_delete=models.CASCADE, related_name='meseros', default=1, editable=False)
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
    #Asociacion:
    restaurante = models.ForeignKey('Restaurante', on_delete=models.CASCADE, related_name='personal_cocina_list', default=1, editable=False)
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
    def preparar_pedido(self, pedido:'Pedido'):
        tiempo_espera = random.randint(10, 20)
        pedido.tiempo_espera = tiempo_espera
        pedido.estado = 'EN_PREPARACION'
        pedido.save()
        return tiempo_espera
    def servir_pedido(self, pedido:'Pedido'):
        pedido.estado = 'SERVIDO'
        pedido.save()
    def __str__(self):
        return self.nombre+' | '+self.identificacion

class Cliente(Persona):
    #Atributos:
    cantidad_persona = models.PositiveIntegerField(editable=False, default=1)
    es_para_llevar = models.BooleanField(editable=False, default=False)
    #Asociacion:
    historial = models.OneToOneField('Historial', on_delete=models.CASCADE, null=True, editable=False,
                                     related_name='cliente')
    mesa = models.OneToOneField('Mesa', on_delete=models.CASCADE, null=True, editable=False)
    restaurante = models.ForeignKey('Restaurante', on_delete=models.CASCADE, related_name='clientes', default=1, editable=False)
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
    #Metodos:
    def save(self, *args, **kwargs):
        if not self.historial:
            historial = Historial.objects.create()
            self.historial = historial
        super().save(*args, **kwargs)

    @staticmethod
    def realizar_pago(pedido:'Pedido', monto:float):
        pedido.estado = Estado.pagado.value
        pedido.save()
    @staticmethod
    def visualizar_mesa_asignada(cliente:'Cliente'):
        return cliente.mesa.numero if cliente.mesa else 'Para llevar'
    def ordenar_pedido(self, es_para_llevar:bool, mesa_ocupada:'Mesa'=None):
        if es_para_llevar:
            self.es_para_llevar = True
            self.mesa = None
        else:
            self.es_para_llevar = False
            self.mesa = mesa_ocupada
        self.save()
        nuevo_pedido = Pedido.objects.create(cliente=self, mesa=self.mesa)
        for item in self.item_pedido_list.all():
            nuevo_pedido.item_pedido_list.add(item)
        nuevo_pedido.save()

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
        return self.plato.nombre+' | '+str(self.cantidad)+' | '+self.observacion

class Pedido(models.Model):
    #Atributos:
    fecha_actual = models.DateTimeField(auto_now=True, editable=False)
    informacion = models.TextField(editable=False)
    numero = models.PositiveIntegerField(editable=False, unique=True)
    tiempo_espera = models.PositiveIntegerField(editable=False, null=True)
    #Asociacion:
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE, related_name='pedidos', default=4)
    estado = models.CharField(max_length=50, choices=[(tag.name, tag.value) for tag in Estado], default=Estado.pendiente.value)
    mesa = models.OneToOneField('Mesa', on_delete=models.CASCADE, null=True, blank=True)
    item_pedido_list = models.ManyToManyField(ItemPedido, blank=True)
    restaurante = models.ForeignKey('Restaurante', on_delete=models.CASCADE, related_name='pedidos', default=1)
    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
    #Metodos:
    def save(self, *args, **kwargs):
        if not self.numero:
            self.numero = Pedido.objects.count() + 1
        super().save(*args, **kwargs)
    def calcular_total(self):
        total = sum(item.plato.precio * item.cantidad for item in self.item_pedido_list.all())
        return round(total, 2)
    def mostrar_tiempo_espera(self):
        if self.tiempo_espera:
            return f"Tiempo de espera: {self.tiempo_espera} minutos"
        return "El pedido aún no ha sido atendido"
    def registrar_informacion(self):
        informacion = f"Pedido N°: {self.numero}\n"
        informacion += f"Fecha: {self.fecha_actual}\n"
        informacion += f"Cliente: {self.cliente.nombre}\n"
        informacion += f"Estado: {self.estado}\n"
        informacion += f"Mesa: {self.mesa.numero if self.mesa else 'Para llevar'}\n"
        informacion += f"Total: {self.calcular_total()}\n"
        informacion += "Items del Pedido:\n"
        for item in self.item_pedido_list.all():
            informacion += f"  - {item.plato.nombre} x {item.cantidad} (Observación: {item.observacion})\n"
        self.informacion = informacion
        self.save()
    def __str__(self):
        return str(self.numero)+' | '+str(self.fecha_actual)+' | '+str(self.estado)+' | '+str(self.mesa.numero)

class Historial(models.Model):
    #Atributos:
    pedidos = models.ManyToManyField(Pedido)
    class Meta:
        verbose_name = "Historial"
        verbose_name_plural = "Historiales"
    #Metodos:
    def __str__(self):
        return str(self.id)+' | '+self.cliente.nombre

class Restaurante(InteraccionCliente):
    #Atributos:
    nombre = models.CharField(max_length=50)
    #Asociacion:
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
    def mostrar_mesas_disponibles(self):
        mesas_disponibles = Mesa.objects.filter(esta_disponible=True, restaurante=self)
        return mesas_disponibles
    def __str__(self):
        return self.nombre
    #Interfaz:
    def asignar_mesa(self, cliente: Cliente, cantidad_persona: int):
        mesas_disponibles = self.mostrar_mesas_disponibles()
        for mesa in mesas_disponibles:
            if mesa.capacidad >= cantidad_persona:
                cliente.mesa = mesa
                mesa.ocupar()
                cliente.save()
                mesa.save()
    def atender_pedido(self):
        pedidos_pendientes = Pedido.objects.filter(estado=Estado.pendiente.value)
        return pedidos_pendientes
    def realizar_reserva(self, cliente: Cliente, fecha: datetime.date, cantidad_persona: int, mesa: 'Mesa' = None):
        if mesa and mesa.capacidad < cantidad_persona:
            raise ValueError("La cantidad de personas excede la capacidad de la mesa.")

        if mesa and Pedido.objects.filter(mesa=mesa, fecha_actual__date=fecha, estado=Estado.reservado.value).exists():
           raise ValueError("La mesa ya está reservada para la fecha indicada.")

        nuevo_pedido = Pedido.objects.create(
           cliente=cliente,
           mesa=mesa,
           estado=Estado.reservado.value,
           fecha_actual=datetime.combine(fecha, datetime.min.time())
        )
        nuevo_pedido.save()
        return nuevo_pedido


class Plato(models.Model):
    #Atributos:
    nombre = models.CharField(max_length=50, unique=True)
    precio = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])
    imagen = models.ImageField(upload_to='platos/', null=True, blank=True)
    #Asociacion:
    menu = models.ForeignKey('Menu', on_delete=models.CASCADE, related_name='platos', default=1, editable=False)
    class Meta:
        verbose_name = "Plato"
        verbose_name_plural = "Platos"
    #Metodos:
    def __str__(self):
        return self.nombre+' | '+str(self.precio)

class Menu(models.Model):
    #Asociacion:
    restaurante = models.OneToOneField('Restaurante', on_delete=models.CASCADE, related_name='menu', default=1, editable=False)
    class Meta:
        verbose_name = "Menu"
        verbose_name_plural = "Menus"
    #Metodos:
    def __str__(self):
        return str(self.id)

class Mesa(models.Model):
    #Atributos:
    capacidad = models.PositiveIntegerField(default=1)
    esta_disponible = models.BooleanField(default=True, editable=False)
    numero = models.PositiveIntegerField(editable=False, unique=True)
    #Asociacion:
    restaurante = models.ForeignKey('Restaurante', on_delete=models.CASCADE, related_name='mesas', default=1, editable=False)
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
    def ocupar(self):
        self.esta_disponible = False
    def __str__(self):
        return str(self.numero)+' | '+str(self.capacidad)+' | '+str(self.esta_disponible)

class RegistroHistorico(models.Model):
    pedidos = models.ManyToManyField(Pedido, editable=False, blank=True)
    #Metodos:
    def __str__(self):
        return str(self.id)+' | '+self.restaurante.nombre