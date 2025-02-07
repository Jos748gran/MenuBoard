from enum import Enum
from django.core.validators import MinValueValidator
from django.db import models
from inventario.models import Insumo

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
    def agregar_cliente(self):
        pass
    def anotar_pedido(self, pedido:'Pedido'):
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
    def entregar_pedido(self, pedido):
        self.actualizar_estado(Estado.servido, pedido)
        print(f"--> El pedido {pedido.numero} fue entregado al cliente {pedido.cliente.nombre}")
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
    def modificar_pedido(self, item_pedido, es_para_eliminar):
        if es_para_eliminar:
            if item_pedido in self.item_pedido_list.all():
                self.item_pedido_list.remove(item_pedido)
            else:
                print("El pedido no posee dicho item")
        else:
            self.item_pedido_list.add(item_pedido)
            print("El item fue agregado al pedido")

    def ocupar_mesa(self, mesa_ocupada):
        self.mesa = mesa_ocupada
        self.save()

    def realizar_pago(self, total, pedido):
        print(f"--> {self.nombre} realizó el pago de ${total}")
        if self.mesa:
            self.historial.agregar_pedido(pedido, self.mesa.numero)
        else:
            self.historial.agregar_pedido(pedido, 0)

        if not self.es_para_llevar:
            self.mesa.desocupar()
            print(f"--> {self.nombre} ha desocupado la mesa {self.mesa.numero}")
            self.mesa = None
            self.save()

        self.item_pedido_list.clear()

    def realizar_pedido(self, es_para_llevar, plato, cantidad, observacion):
        self.es_para_llevar = es_para_llevar
        self.realizo_pedido = False
        item_pedido = ItemPedido(cliente=self, plato=plato, cantidad=cantidad, observacion=observacion)
        item_pedido.save()
        self.item_pedido_list.add(item_pedido)

        if observacion.lower() == "ninguna":
            print(f"-> {self.nombre} pidió [{cantidad}] ({plato.nombre})")
        else:
            print(f"-> {self.nombre} pidió [{cantidad}] ({plato.nombre}) {{{observacion}}}")

        self.realizo_pedido = True
        self.save()

    def visualizar_mesa_asignada(self):
        if self.mesa:
            print(
                f"---> A {self.nombre} se le asignó la mesa (Número: {self.mesa.numero} | Capacidad: {self.mesa.capacidad} personas)")

    def __str__(self):
        return self.nombre + ' | ' + self.cedula

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
    estado = models.CharField(max_length=50, choices=[(tag.name, tag.value) for tag in Estado], default=Estado.pendiente.name)
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
    def agregar_item(self, item_pedido):
        self.item_pedido_list.add(item_pedido)

    def calcular_total(self):
        total = 0
        for item_pedido in self.item_pedido_list.all():
            total += item_pedido.cantidad * item_pedido.plato.precio
        return total

    def mostrar_tiempo_espera(self, tiempo, item_pedido):
        print(f"-> El plato de ({item_pedido.plato.nombre}) estará en {tiempo} minutos")

    def registrar_informacion(self, numero_mesa):
        if numero_mesa == 0:
            self.informacion = f"| Nombre: {self.cliente.nombre} | Fecha: {self.fecha_actual} | Pedido: {self.numero} | Para Llevar: {self.cliente.is_es_para_llevar()} | Total: {self.calcular_total()} |"
        else:
            self.informacion = f"| Nombre: {self.cliente.nombre} | Fecha: {self.fecha_actual} | Pedido: {self.numero} | Nro.Personas: {self.cliente.get_cantidad_personas()} | Para Llevar: {self.cliente.is_es_para_llevar()} | Mesa: {numero_mesa} | Total: {self.calcular_total()} |"

    def remover_item(self, item_pedido):
        if item_pedido in self.item_pedido_list.all():
            self.item_pedido_list.remove(item_pedido)

    def __str__(self):
        return f"Pedido: {self.numero}"

class Historial(models.Model):
    #Atributos:
    pedidos = models.ManyToManyField(Pedido)
    class Meta:
        verbose_name = "Historial"
        verbose_name_plural = "Historiales"
    #Metodos:
    def agregar_pedido(self, pedido, numero_mesa):
        self.pedidos.add(pedido)
        pedido.registrar_informacion(numero_mesa)
        print(f"--> Pedido {pedido.numero} agregado al historial del cliente.")

    def mostrar_informacion(self):
        if not self.pedidos.exists():
            print("¡El cliente no tiene pedidos en su historial!")
        else:
            print("---------------------------------------------- Historial de pedidos ----------------------------------------------")
            for pedido in self.pedidos.all():
                print(pedido.informacion)
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
    imagen = models.ImageField(upload_to='platos/', null=True, blank=True)
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
    def agregar_plato(self, nombre, precio):
        self.platos.append(Plato(nombre, precio))

    def mostrar_platos(self):
        print("|-------- Platos disponibles --------|")
        for plato in self.platos:
            print(f"[ Plato: {plato.get_nombre()} | Precio: ${plato.get_precio()} ]")
        print("|____________________________________|")

    def remover_plato(self, plato_remover):
        self.platos = [plato for plato in self.platos.all() if plato != plato_remover]
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
        self.save()

    def reservar(self):
        self.esta_disponible = False
        self.save()
    def __str__(self):
        return str(self.numero)+' | '+str(self.capacidad)+' | '+str(self.esta_disponible)

class RegistroHistorico(models.Model):
    pedidos = models.ManyToManyField(Pedido, editable=False, blank=True)
    # Métodos:
    def registrar_pedido(self, pedido):
        self.pedidos.add(pedido)
        print(f"{{ Pedido {pedido.numero} guardado en el Registro del restaurante }}")

    def mostrar_lista_pedidos(self):
        print("[------- Registro Historico -------]")
        for pedido in self.pedidos.all():
            print(f"| Pedido: {pedido.numero} | Fecha: {pedido.fecha_actual} |")
        print("[__________________________________]")

    def __str__(self):
        return str(self.id) + ' | ' + self.restaurante.nombre
