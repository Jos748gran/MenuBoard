from django.contrib import admin
from .models import Mesa, Persona, Cliente, Personal, Reserva
from django.utils.html import format_html



@admin.register(Mesa)
class MesaAdmin(admin.ModelAdmin):
    list_display = ('identificador', 'numero_asientos', 'ubicacion', 'estado', 'hora_disponible')
    list_filter = ('estado', 'ubicacion')
    search_fields = ('identificador', 'ubicacion')
    list_editable = ('estado',)



@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    search_fields = ('nombre', 'cedula_persona', 'email')
    list_display = ('nombre', 'cedula_persona', 'email', 'telefono')



@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    search_fields = ('nombre', 'cedula_persona', 'email')
    list_display = ('nombre', 'cedula_persona', 'email')
   # Puedes añadir un filtro personalizado dependiendo de relaciones.



@admin.register(Personal)
class PersonalAdmin(admin.ModelAdmin):
    list_display = ('nombre','identificador_Personal', 'cedula_persona', 'email', 'rol')
    list_filter = ('rol',)
    search_fields = ('nombre', 'email')



from datetime import timedelta

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('identificador', 'cliente', 'mesa', 'estado', 'fecha_reserva', 'horario_inicio', 'hora_reserva_finalizada', 'duracion')
    list_filter = ('estado', 'fecha_reserva')
    search_fields = (
        'identificador',
        'cliente__nombre',
        'mesa__identificador',
        'cliente__email',
        'cliente__telefono',
        'estado',
        'fecha_reserva',
    )
    ordering = ('fecha_reserva', 'horario_inicio')
    list_editable = ('estado', 'mesa')

    # Campo calculado para la duración de la reserva
    def duracion(self, obj):
        if obj.hora_reserva_finalizada and obj.horario_inicio:
            duracion = obj.hora_reserva_finalizada - obj.horario_inicio
            # Retorna en formato horas:minutos
            return str(timedelta(seconds=duracion.total_seconds()))
        return "Sin finalizar"
    duracion.short_description = "Duración"

    # Campo coloreado para el estado con icono
    def estado_coloreado(self, obj):
        colores = {
            'CONFIRMADA': ('green', '✔️'),
            'CANCELADA': ('red', '❌'),
            'FINALIZADA': ('blue', '✅'),
            'ENCURSO': ('orange', '⏳'),
        }
        color, icono = colores.get(obj.estado, ('black', '❔'))
        return format_html(
            '<span style="color: {};">{} {}</span>',
            color,
            icono,
            obj.estado
        )
    estado_coloreado.short_description = "Estado"

    def cancelar_reserva(self, request, queryset):
        """
        Acción personalizada para cancelar reservas desde el admin.
        """
        for reserva in queryset:
            reserva.cancelar_reserva(reserva.identificador)
        self.message_user(request, f"{queryset.count()} reserva(s) cancelada(s) correctamente.")

    actions = ['cancelar_reserva']  # Registra la acción en el admin.
