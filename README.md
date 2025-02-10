# Sistema de Gestión de Pedidos de Restaurante

Este proyecto tiene como objetivo implementar el módulo de Pedidos dentro de un sistema de gestión para un restaurante. El sistema está basado en un diagrama UML diseñado en la Unidad 1, que incluye los conceptos fundamentales de la programación orientada a objetos (POO), tales como la abstracción, encapsulación, herencia y polimorfismo.

## Estructura del Proyecto

El sistema está compuesto por 6 módulos principales, cada uno enfocado en diferentes aspectos del restaurante. Estos módulos son:

1. **Gestor de Clientes**: Maneja la información y las operaciones relacionadas con los clientes.
2. **Gestor de Mesas**: Administra la disponibilidad y asignación de mesas.
3. **Menú y Platos**: Permite la gestión de los platos ofrecidos por el restaurante.
4. **Personal del Restaurante**: Incluye la gestión del personal de cocina y meseros.
5. **Historial de Operaciones**: Almacena un registro de las operaciones realizadas.
6. **Módulo de Pedidos**: Responsable de gestionar los pedidos realizados por los clientes.

### Módulo de Pedidos

El módulo de Pedidos tiene las siguientes responsabilidades principales:

- **Gestión de Pedidos**: Registrar los pedidos realizados por los clientes, especificando los elementos solicitados, cantidades y observaciones.
- **Cálculo de Factura**: Calcular el total de los pedidos realizados.
- **Seguimiento de Estado**: Actualizar y visualizar el estado de los pedidos (e.g., EN_PREPARACION, SERVIDO, PAGADO).

### Implementación de POO

Los conceptos de abstracción y encapsulación se implementan a través de las clases principales que representan las entidades del sistema, tales como:

- **Cliente**: Representa a los clientes del restaurante.
- **Pedido**: Contiene información sobre los pedidos realizados.
- **ItemPedido**: Representa cada elemento del pedido.
- **PersonalCocina** y **Mesero**: Modelan al personal del restaurante.

El polimorfismo y la herencia también se emplean para garantizar que las interacciones entre clases sean flexibles y escalables.

## Diagrama UML

El siguiente diagrama UML describe la estructura del sistema. Este fue actualizado durante el desarrollo para reflejar los cambios realizados:

![Diagrama UML](https://github.com/user-attachments/assets/ae33e66d-7f59-4cef-b792-bfeb138b42ed)

El diagrama muestra las clases principales, sus atributos y métodos, así como las relaciones entre ellas, como agregaciones, composiciones y asociaciones.

## Uso del Sistema

1. **Registro de Clientes**: Los clientes pueden ser registrados en el sistema mediante sus datos personales.
2. **Creación de Pedidos**: Los pedidos pueden ser realizados indicando los platos y cantidades.
3. **Asignación de Mesas**: Los clientes pueden ser asignados a mesas disponibles.
4. **Seguimiento de Pedidos**: El personal puede actualizar y consultar el estado de los pedidos.

## Diseño adecuado de la GUI

```markdown
### Diseño adecuado de la GUI

#### Formularios

Los formularios son esenciales para la interacción del usuario con el sistema. En Django, se pueden crear formularios utilizando `forms.py`. Aquí hay un ejemplo de cómo definir formularios para las operaciones CRUD:

```python
# forms.py
from django import forms
from .models import Cliente, Pedido, ItemPedido

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['cedula', 'nombre', 'telefono', 'cantidad_persona']

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['cliente', 'mesa', 'estado']

class ItemPedidoForm(forms.ModelForm):
    class Meta:
        model = ItemPedido
        fields = ['cliente', 'plato', 'cantidad', 'observacion']
```

#### Botones y Menús

Los botones y menús se definen en las plantillas HTML. Aquí hay un ejemplo de cómo crear un formulario con botones en una plantilla HTML:

```html
<!-- templates/crear_cliente.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Crear Cliente</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
</head>
<body>
    <div class="container">
        <h2>Crear Cliente</h2>
        <form method="post">
            {% csrf_token %}
            {{ form.as_p }}
            <button type="submit" class="btn btn-primary">Guardar</button>
        </form>
    </div>
</body>
</html>
```

### Conectividad de la GUI con el backend

#### Vistas

Las vistas en `views.py` manejan las solicitudes HTTP y conectan los formularios con los modelos de la base de datos. Aquí hay un ejemplo de vistas para las operaciones CRUD:

```python
# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ClienteForm, PedidoForm, ItemPedidoForm
from .models import Cliente, Pedido, ItemPedido

def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes')
    else:
        form = ClienteForm()
    return render(request, 'crear_cliente.html', {'form': form})

def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'lista_clientes.html', {'clientes': clientes})

def modificar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'modificar_cliente.html', {'form': form})

def eliminar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        cliente.delete()
        return redirect('lista_clientes')
    return render(request, 'eliminar_cliente.html', {'cliente': cliente})
```

### Funcionalidad: Operaciones CRUD

La interfaz debe permitir realizar las operaciones CRUD (Crear, Leer, Actualizar, Eliminar) en la base de datos. Los ejemplos anteriores muestran cómo crear, listar, modificar y eliminar clientes.

### Calidad estética y usabilidad de la interfaz

Para mejorar la apariencia y usabilidad de la interfaz, se pueden utilizar CSS y frameworks como Bootstrap. Aquí hay un ejemplo de cómo incluir Bootstrap en una plantilla HTML:

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}Mi Aplicación{% endblock %}</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
</head>
<body>
    <div class="container">
        {% block content %}
        {% endblock %}
    </div>
</body>
</html>
```

Luego, extiende esta plantilla en otras plantillas para mantener un diseño consistente:

```html
<!-- templates/crear_cliente.html -->
{% extends 'base.html' %}

{% block title %}Crear Cliente{% endblock %}

{% block content %}
<h2>Crear Cliente</h2>
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit" class="btn btn-primary">Guardar</button>
</form>
{% endblock %}
```


# Reflexión del Proceso de Implementación, Integración y Pruebas

Este documento describe detalladamente el proceso llevado a cabo en el desarrollo del proyecto, abarcando desde la implementación de la interfaz gráfica, la integración con la base de datos, el uso de APIs externas y librerías, hasta las pruebas de integración realizadas para garantizar el correcto funcionamiento del sistema.

---

## 1. Implementación de la Interfaz Gráfica

Para la creación de la interfaz gráfica se optó por un diseño web moderno y responsivo, utilizando tecnologías como **HTML5**, **CSS3** y **JavaScript**. Se estructuró la página de forma modular para facilitar el mantenimiento y futuras ampliaciones, prestando especial atención a la experiencia de usuario. Algunos aspectos destacados fueron:

- **Diseño Responsivo:** Se utilizó un enfoque adaptable para que la interfaz se visualice correctamente en diferentes dispositivos y tamaños de pantalla.
- **Accesibilidad e Interactividad:** Se implementaron controles intuitivos, botones y formularios que permiten al usuario interactuar de forma sencilla con la aplicación.
- **Modularidad:** La división del código en componentes o secciones facilitó la integración con el resto de módulos del sistema, como la comunicación con la base de datos y las APIs externas.

![Home](https://github.com/user-attachments/assets/a1840304-0439-4ff8-b7a4-4537c52f3c15)
>Home

![Menu](https://github.com/user-attachments/assets/cf76bd2b-6a7b-4618-8d40-ba0e5de125bb)
>Menu

![Login](https://github.com/user-attachments/assets/1c1b8994-aec9-4d13-9e25-f1f539aeaeea)
>Autenticacion de usuario

![image](https://github.com/user-attachments/assets/4418da47-1c8b-45ec-aba0-70d6672f0418)
>Creacion de una cuenta


Esta aproximación permitió desarrollar una interfaz atractiva y funcional, que se conecta de manera efectiva con los servicios en el backend.

---

## 2. Integración con la Base de Datos (PostgreSQL)

La persistencia de la información se logró mediante la utilización de **PostgreSQL**, un sistema de gestión de bases de datos relacional robusto y escalable. El proceso incluyó los siguientes pasos:

- **Diseño de la Base de Datos:** Se definieron las tablas, relaciones e índices necesarios para almacenar de forma eficiente la información requerida por la aplicación.
- **Conexión y Comunicación:** Se configuró la conexión entre el backend y PostgreSQL utilizando librerías específicas (por ejemplo, *psycopg2* en Python o el uso de JDBC en Java), garantizando una comunicación segura y optimizada.
- **Consultas y Transacciones:** Se implementaron operaciones CRUD (crear, leer, actualizar y eliminar) y transacciones que aseguran la integridad de los datos, permitiendo realizar operaciones complejas de manera eficiente.
  
![postgsql](https://github.com/user-attachments/assets/7c60d8ec-93d9-4fe9-81d8-6a1045ff26f3)
>Base de datos


Esta integración fue fundamental para respaldar las funcionalidades de la aplicación y para asegurar que los datos se gestionen de forma consistente y confiable.

---

## 3. Uso de APIs y Librerías Estándar

Para enriquecer la experiencia del usuario y proporcionar funcionalidades avanzadas sin desarrollar soluciones desde cero, se integraron APIs externas:

### a) Google Maps API
![maps](https://github.com/user-attachments/assets/3f947ede-44e4-419c-923c-ac3ece4772dc)
>Google Maps
Se utilizó la API de Google Maps para incorporar mapas interactivos dentro de la aplicación. Esto se logró mediante la inclusión del siguiente script en el HTML:

```html
<script async defer 
        src="https://maps.googleapis.com/maps/api/js?key={{ google_maps_api_key }}&callback=initMap"></script>
```

- **Carga Asíncrona y Diferida:** Las etiquetas `async` y `defer` aseguran que la carga del script no bloquee la renderización de la página, mejorando el rendimiento.
- **Callback `initMap`:** Una vez cargada la API, se llama a la función `initMap`, encargada de inicializar y configurar el mapa según los requerimientos del proyecto.
- **Seguridad y Gestión de Claves:** El uso de `{{ google_maps_api_key }}` permite gestionar la clave de forma segura, evitando exponer datos sensibles en el código fuente.

### b) Integración de Meteoblue Mediante Iframe

Para mostrar información meteorológica, se integró un iframe que carga datos desde Meteoblue:

```html
<iframe src="{{ meteoblue_url }}" frameborder="0" scrolling="NO" allowtransparency="true"
        sandbox="allow-same-origin allow-scripts allow-popups allow-popups-to-escape-sandbox"
        style="width: 100%; height: 720px"></iframe>
```

- **Sandboxing:** La propiedad `sandbox` limita las acciones permitidas en el contenido del iframe, aumentando la seguridad al evitar que el contenido externo ejecute código malicioso.
- **Responsive y Visual:** Se establecieron estilos para que el iframe ocupe el 100% del ancho y tenga una altura adecuada, permitiendo una visualización óptima de los datos meteorológicos.
![image](https://github.com/user-attachments/assets/8f33fb4e-b651-4cb9-bca3-b72d621b60d2)
>MeteoBlue


La integración de estas APIs facilitó la incorporación de funcionalidades avanzadas, como la visualización de mapas y datos en tiempo real, sin incrementar significativamente la complejidad del desarrollo.

---

## 4. Pruebas de Integración

Las pruebas de integración fueron esenciales para garantizar que todos los componentes del sistema funcionaran de manera conjunta y sin errores. Se llevaron a cabo diversas estrategias:

- **Validación de la Interfaz Gráfica:** Se verificó que los elementos de la interfaz respondieran correctamente a las interacciones del usuario, asegurando que las llamadas a las APIs se ejecutaran sin problemas y que los datos se actualizaran en tiempo real.
- **Pruebas de Comunicación con la Base de Datos:** Se realizaron pruebas para confirmar que las operaciones CRUD en PostgreSQL se ejecutaban correctamente, comprobando la integridad y consistencia de los datos.
- **Verificación de las APIs Externas:**
  - **Google Maps:** Se comprobó la correcta carga del mapa, la inicialización de la función `initMap` y la interacción del usuario con los elementos del mapa (como marcadores y ventanas informativas).
  - **Meteoblue Iframe:** Se testeo que el iframe mostrara la información meteorológica de forma dinámica y que las restricciones del sandbox garantizaran la seguridad del contenido.
---

## Conclusión

La implementación de este proyecto supuso un reto integral que involucró el diseño y desarrollo de una interfaz gráfica moderna, la integración con una base de datos robusta como PostgreSQL y la incorporación de funcionalidades avanzadas mediante APIs externas (Google Maps y Meteoblue). La realización de pruebas exhaustivas aseguró la calidad y estabilidad del sistema.

