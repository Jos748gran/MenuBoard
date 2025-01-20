from django.db import models

# Create your models here.

from django.db.models.signals import post_save
from django.dispatch import receiver


from abc import ABC, abstractmethod


class GestionInventario(ABC):
    @abstractmethod
    def agregar_item(self, item):
        """Agregar un nuevo ítem al inventario."""
        pass

    @abstractmethod
    def eliminar_item(self, item):
        """Eliminar un ítem del inventario."""
        pass

    @abstractmethod
    def buscar_items(self):
        """Listar todos los ítems en el inventario."""
        pass

    @abstractmethod
    def actualizar(self):
        pass

class Insumo(models.Model):
    identificador = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=50)
    cantidadDisponible = models.IntegerField(default=0)
    unidadMedida = models.CharField(max_length=30)
    nivelReorden = models.IntegerField()
    precioUnitario = models.FloatField()
    ubicacion = models.CharField(max_length=100)

    def str(self):
        return f"{self.identificador} - {self.nombre} ({self.cantidadDisponible} {self.unidadMedida})"

    def verificar_nivel_reorden(self):
        """Genera una alerta si la cantidad disponible está por debajo del nivel de reorden."""
        if self.cantidadDisponible < self.nivelReorden:
            Alerta.objects.create(
                mensaje=f"Insumo '{self.nombre}' bajo el nivel de reorden, reabastezca.",
                fecha=models.DateTimeField.now(),
                tipo='bajo_stock'
            )


class Operacion(models.Model):
    TIPO_OPERACION_CHOICES = [
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
    ]
    tipo = models.CharField(max_length=10, choices=TIPO_OPERACION_CHOICES)
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE, related_name="operaciones")
    cantidad = models.IntegerField()
    fechaRegistro = models.DateTimeField(auto_now_add=True)
    observaciones = models.TextField(blank=True, null=True)

    def str(self):
        return f"Operación {self.tipo} - {self.insumo.nombre} ({self.cantidad} {self.insumo.unidadMedida})"


class Historial(models.Model):
    operacion = models.OneToOneField(Operacion, on_delete=models.CASCADE)
    descripcion = models.TextField()

    def str(self):
        return f"Registro del {self.operacion.fechaRegistro}"


class Alerta(models.Model):
    mensaje = models.CharField(max_length=255)
    fecha = models.DateTimeField(auto_now_add=True)
    TIPO_ALERTA_CHOICES = [
        ('bajo_stock', 'Bajo Stock'),
        ('vencimiento', 'Vencimiento'),
    ]
    tipo = models.CharField(max_length=50, choices=TIPO_ALERTA_CHOICES)

    def str(self):
        return f"Alerta: {self.tipo} - {self.mensaje} ({self.fecha})"


class ReporteConsumo(models.Model):
    periodoInicio = models.DateField()
    periodoFin = models.DateField()
    datos = models.TextField(blank=True)

    def generarReporte(self):
        """Generar un reporte con los insumos más utilizados."""
        operaciones = Operacion.objects.filter(
            tipo='salida',
            fechaRegistro__range=(self.periodoInicio, self.periodoFin)
        ).values('insumo__nombre').annotate(total=models.Sum('cantidad')).order_by('-total')

        reporte = "\n".join([f"{op['insumo__nombre']}: {op['total']} unidades" for op in operaciones])
        self.datos = reporte
        self.save()
        return reporte

    def str(self):
        return f"Reporte de consumo ({self.periodoInicio} a {self.periodoFin})"


class Inventario(models.Model):
    almacenamiento = models.CharField(max_length=200)

    def str(self):
        return self.almacenamiento


class Administrador(models.Model):
    revision = models.TextField()
    control = models.TextField()

    def crearReporte(self):
        pass


class ReporteBodega(models.Model):
    tipo = models.CharField(max_length=100)
    datos = models.TextField()

    def generarReporte(self):
        pass

    def actualizarReporte(self):
        pass

    def str(self):
        return f"Reporte de bodega ({self.tipo})"


class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    direccion = models.CharField(max_length=255)
    contacto = models.CharField(max_length=100)

    def str(self):
        return f"{self.nombre} - {self.contacto}"


class Pedido(models.Model):
    cliente = models.CharField(max_length=255)
    fecha = models.DateField()
    ESTADO_PEDIDO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    ]
    estado = models.CharField(max_length=50, choices=ESTADO_PEDIDO_CHOICES)

    def str(self):
        return f"Pedido de {self.cliente} - {self.estado} ({self.fecha})"


class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()

    def str(self):
        return self.nombre


class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    rol = models.CharField(max_length=50)
    email = models.EmailField()

    def str(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.FloatField()

    def str(self):
        return self.nombre


class Persona(models.Model):
    edad = models.IntegerField()
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)

    def str(self):
        return f"{self.nombre} {self.apellido}"


@receiver(post_save, sender=Operacion)
def actualizar_inventario(sender, instance, **kwargs):
    """Actualizar la cantidad disponible en los insumos con cada operación de inventario."""
    insumo = instance.insumo
    if instance.tipo == 'entrada':
        insumo.cantidadDisponible += instance.cantidad
    elif instance.tipo == 'salida':
        insumo.cantidadDisponible -= instance.cantidad
    insumo.save()

    # Registrar en el historial
    Historial.objects.create(
        operacion=instance,
        descripcion=f"Se realizó una operación de tipo {instance.tipo} con {instance.cantidad} de '{insumo.nombre}'."
    )

    # Verificar niveles de reorden después de actualizar el inventario
    insumo.verificar_nivel_reorden()