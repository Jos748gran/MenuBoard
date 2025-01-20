
from django.db import models
from enum import Enum
from django.db.models import Manager
from abc import ABC, abstractmethod


class EstadoMesa(Enum):
    LIBRE = "LIBRE"
    OCUPADA = "OCUPADA"
    RESERVADA = "RESERVADA"

class EstadoReserva(Enum):
    CONFIRMADA = "CONFIRMADA"
    CANCELADA = "CANCELADA"
    FINALIZADA = "FINALIZADA"
    ENCURSO = "ENCURSO"

class Rol(Enum):
    MESERO = "MESERO"
    SECRETARIO = "SECRETARIO"

# Modelos
class Mesa(models.Model):
    identificador = models.CharField(max_length=50)
    numero_asientos = models.IntegerField()
    ubicacion = models.CharField(max_length=100)
    estado = models.CharField(
        max_length=10,
        choices=[(tag.name, tag.value) for tag in EstadoMesa],
        default=EstadoMesa.LIBRE.name,
        verbose_name="Estado"
    )
    mesas_unidas: Manager = models.ManyToManyField('self', blank=True, symmetrical=False)
    hora_disponible = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Mesa {self.identificador} - Capacidad {self.numero_asientos}"

    def cambiar_estado(self, nuevo_estado):
        """
        Cambia el estado de la mesa al nuevo estado dado, validando que sea un estado aceptado.
        """
        if nuevo_estado not in [estado.name for estado in EstadoMesa]:
            raise ValueError(
                f"Estado '{nuevo_estado}' no es válido. Los estados válidos son: {[estado.name for estado in EstadoMesa]}")
        self.estado = nuevo_estado
        self.save()
    def validar_Disponibilidad(self, horario_inicio):
        return self.hora_disponible > horario_inicio



class Persona(models.Model):
    nombre = models.CharField(max_length=100)
    cedula_persona = models.CharField(max_length=10, unique=True)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, unique=True)

class Cliente(Persona):
    activo = models.BooleanField(default=True, verbose_name="Estado activo")

    def __str__(self):
        return self.nombre

    def actualizar_informacion(self, nombre, email, telefono):
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
        self.save()

    def ver_reservas(self):
        return self.reserva_set.all()

    def consultar_disponibilidad(self, mesa):
        return mesa.validar_disponibilidad()

    def activar_cliente(self):
        """
        Activa al cliente si está inactivo.
        """
        if not self.activo:
            self.activo = True
            self.save()

    def desactivar_cliente(self):
        """
        Desactiva al cliente si está activo.
        """
        if self.activo:
            self.activo = False
            self.save()

    def hacer_reserva(self, datos_reserva):
        """
        Crear una nueva reserva asociada al cliente.
        """
        reserva = Reserva.objects.create(
            cliente=self,
            mesa=datos_reserva['mesa'],
            cantidad_personas=datos_reserva['cantidad_personas'],
            fecha_reserva=datos_reserva['fecha_reserva'],
            horario_inicio=datos_reserva['horario_inicio']
        )
        reserva.save()
        return reserva

    def cancelar_reserva(self, identificador_reserva):
        """
        Cancelar una reserva existente asociada al cliente.
        """
        try:
            reserva = Reserva.objects.get(identificador=identificador_reserva, cliente=self)
            reserva.estado = EstadoReserva.CANCELADA.name
            reserva.save()
        except Reserva.DoesNotExist:
            raise ValueError("No se encontró la reserva especificada o no pertenece a este cliente.")


class Reserva(models.Model):
    identificador = models.CharField(max_length=50)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE)
    cantidad_personas = models.IntegerField()
    fecha_reserva = models.DateField()
    horario_inicio = models.DateTimeField()
    hora_reserva_finalizada = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(
        max_length=15,
        choices=[(tag.name, tag.value) for tag in EstadoReserva],
        default=EstadoReserva.CONFIRMADA.name
    )
    def __str__(self):
        return f"Reserva {self.cliente.nombre}"

    def modificar_reserva(self, nuevos_datos):
        for key, value in nuevos_datos.items():
            setattr(self, key, value)
        self.save()

    def verificar_disponibilidad(self, mesa, fecha, horario_inicio):
        return mesa.validar_disponibilidad(horario_inicio)

    def finalizar_reserva(self):
        self.estado = EstadoReserva.FINALIZADA.name
        self.save()

    def hacer_reserva(self, datos_reserva):
        """
        Crear una nueva reserva basada en los datos proporcionados.
        """
        reserva = Reserva.objects.create(
            cliente=datos_reserva['cliente'],
            mesa=datos_reserva['mesa'],
            cantidad_personas=datos_reserva['cantidad_personas'],
            fecha_reserva=datos_reserva['fecha_reserva'],
            horario_inicio=datos_reserva['horario_inicio']
        )
        reserva.save()
        return reserva

    def cancelar_reserva(self, identificador_reserva):
        """
        Cancelar la reserva actual si coincide con el identificador.
        """
        if self.identificador == identificador_reserva:
            self.estado = EstadoReserva.CANCELADA.name
            self.save()
        else:
            raise ValueError("El identificador de reserva no coincide.")

class Personal(Persona):
    identificador_Personal = models.CharField(max_length=50, unique=True)
    rol = models.CharField(
        max_length=15,
        choices=[(tag.name, tag.value) for tag in Rol],
        default=Rol.MESERO.name
    )
    def notificar_Mesa_Lista(self, mesas):
        pass

    def __str__(self):
        return f"{self.nombre} ({self.rol})"

class iReserva(ABC):
    @abstractmethod
    def hacer_reserva(self, datos_reserva):
        """
        Realizar una nueva reserva.
        Parámetros:
        - datos_reserva: dict con la información necesaria para crear la reserva.
        """
        pass

    @abstractmethod
    def cancelar_reserva(self, identificador_reserva):
        """
        Cancelar una reserva existente.
        Parámetros:
        - identificador_reserva: ID único de la reserva a cancelar.
        """
        pass