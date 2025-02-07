from django.db import models

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

