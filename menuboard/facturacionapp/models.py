from django.db import models
from datetime import date
from pedidos.models import *


# Modelo para los impuestos
class Impuesto(models.Model):
    nombre = models.CharField(max_length=50)  # Ejemplo: IVA, ICE
    porcentaje = models.FloatField()  # Por ejemplo: 12.0 para el IVA
    descripcion = models.TextField(blank=True, null=True)  # Opcional para más detalles

    def _str_(self):
        return f"{self.nombre} - {self.porcentaje}%"





# Modelo para los productos
class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    precio = models.FloatField()
    descripcion = models.TextField()
    impuestos = models.ManyToManyField(Impuesto, blank=True)  # Relación con impuestos

    def precio_con_impuestos(self):
        total_impuesto = sum([imp.porcentaje for imp in self.impuestos.all()])
        return self.precio * (1 + total_impuesto / 100)

    def _str_(self):
        return self.nombre

    def actualizar_precio(self, nuevo_precio):
        self.precio = nuevo_precio
        self.save()




# Modelo para la promocion
class Promocion(models.Model):
    descripcion = models.CharField(max_length=255)
    porcentaje_descuento = models.FloatField()

    def _str_(self):
        return self.descripcion


# Modelo para la factura
class Factura(models.Model):
    numero = models.AutoField(primary_key=True)
    total = models.FloatField(default=0.0)
    subtotal = models.FloatField(default=0.0)
    impuesto_total = models.FloatField(default=0.0)
    descuento = models.FloatField(default=0.0)
    fecha = models.DateField(default=date.today)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    metodo_pago_efectivo = models.ForeignKey('PagoEfectivo', null=True, blank=True, on_delete=models.SET_NULL)
    metodo_pago_tarjeta = models.ForeignKey('PagoTarjeta', null=True, blank=True, on_delete=models.SET_NULL)
    metodo_pago_transferencia = models.ForeignKey('PagoTransferencia', null=True, blank=True, on_delete=models.SET_NULL)
    promocion = models.ForeignKey('Promocion', null=True, blank=True, on_delete=models.SET_NULL)

    def calcular_impuesto_total(self):
        impuesto_total = 0.0
        for item in self.pedido.itempedido_set.all():
            for impuesto in item.producto.impuestos.all():
                impuesto_total += item.subtotal() * (impuesto.porcentaje / 100)
        return impuesto_total

    def calcular_monto_total(self):
        self.subtotal = self.pedido.total_pedido()
        self.descuento = self.pedido.total_pedido() * (self.promocion.porcentaje_descuento / 100) if self.promocion else 0.0
        self.impuesto_total = self.calcular_impuesto_total()
        self.total = self.subtotal - self.descuento + self.impuesto_total

    def save(self, *args, **kwargs):
        self.calcular_monto_total()
        super().save(*args, **kwargs)

    def _str_(self):
        return f"Factura {self.numero} para Pedido {self.pedido.numero} - Cliente: {self.pedido.cliente.nombre} ({self.pedido.cliente.cedula})"


# Modelo para los items de factura
class ItemFactura(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, related_name="items")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    subtotal = models.FloatField()

    def calcular_subtotal(self):
        self.subtotal = self.cantidad * self.producto.precio

    def save(self, *args, **kwargs):
        self.calcular_subtotal()
        super().save(*args, **kwargs)

    def _str_(self):
        return f"{self.producto.nombre} x {self.cantidad}"


# Modelo abstracto para metodos de pago
class MetodoDePago(models.Model):
    monto_pagado = models.FloatField()
    cuenta_por_cobrar = models.FloatField()

    class Meta:
        abstract = True


# Modelo para el pago por transferencia
class PagoTransferencia(MetodoDePago):
    numero_transferencia = models.CharField(max_length=50)
    banco_origen = models.CharField(max_length=255)


# Modelo para el pago en efectivo
class PagoEfectivo(MetodoDePago):
    cambio = models.FloatField()


# Modelo para el pago con tarjeta
class PagoTarjeta(MetodoDePago):
    numero_tarjeta = models.CharField(max_length=16)
    titular = models.CharField(max_length=255)
    vencimiento = models.DateField()


# Modelo para el historial de facturas
class HistorialDeFactura(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)

    @classmethod
    def consultar_por_fecha(cls, fecha_inicio, fecha_fin):
        return cls.objects.filter(factura_fecha_range=[fecha_inicio, fecha_fin])

    @classmethod
    def consultar_por_cliente(cls, cliente):
        return cls.objects.filter(factura_pedido_cliente=cliente)

    def _str_(self):
        return f"Historial de Factura {self.factura.numero}"