# Sistema de Gestión de Pedidos de Restaurante

Este proyecto tiene como objetivo implementar el módulo de Pedidos dentro de un sistema de gestión para un restaurante. El sistema está basado en un diagrama UML diseñado en la Unidad 1, que incluye los conceptos fundamentales de la programación orientada a objetos (POO), tales como la abstracción, encapsulación, herencia y polimorfismo.

## Estructura del Proyecto

El sistema está compuesto por 6 módulos principales, cada uno enfocado en diferentes aspectos del restaurante. Estos módulos son:

1. *Gestor de Clientes*: Maneja la información y las operaciones relacionadas con los clientes.
2. *Gestor de Mesas*: Administra la disponibilidad y asignación de mesas.
3. *Menú y Platos*: Permite la gestión de los platos ofrecidos por el restaurante.
4. *Personal del Restaurante*: Incluye la gestión del personal de cocina y meseros.
5. *Historial de Operaciones*: Almacena un registro de las operaciones realizadas.
6. *Módulo de Pedidos*: Responsable de gestionar los pedidos realizados por los clientes.

### Módulo de Pedidos

El módulo de Pedidos tiene las siguientes responsabilidades principales:

- *Gestión de Pedidos*: Registrar los pedidos realizados por los clientes, especificando los elementos solicitados, cantidades y observaciones.
- *Cálculo de Factura*: Calcular el total de los pedidos realizados.
- *Seguimiento de Estado*: Actualizar y visualizar el estado de los pedidos (e.g., EN_PREPARACION, SERVIDO, PAGADO).

### Implementación de POO

Los conceptos de abstracción y encapsulación se implementan a través de las clases principales que representan las entidades del sistema, tales como:

- *Cliente*: Representa a los clientes del restaurante.
- *Pedido*: Contiene información sobre los pedidos realizados.
- *ItemPedido*: Representa cada elemento del pedido.
- *PersonalCocina* y *Mesero*: Modelan al personal del restaurante.

El polimorfismo y la herencia también se emplean para garantizar que las interacciones entre clases sean flexibles y escalables.

## Diagrama UML

El siguiente diagrama UML describe la estructura del sistema. Este fue actualizado durante el desarrollo para reflejar los cambios realizados:

![image](https://github.com/user-attachments/assets/ae33e66d-7f59-4cef-b792-bfeb138b42ed)

El diagrama muestra las clases principales, sus atributos y métodos, así como las relaciones entre ellas, como agregaciones, composiciones y asociaciones.

## Uso del Sistema

1. *Registro de Clientes*: Los clientes pueden ser registrados en el sistema mediante sus datos personales.
2. *Creación de Pedidos*: Los pedidos pueden ser realizados indicando los platos y cantidades.
3. *Asignación de Mesas*: Los clientes pueden ser asignados a mesas disponibles.
4. *Seguimiento de Pedidos*: El personal puede actualizar y consultar el estado de los pedidos.
5. *Cálculo de Facturas*: El sistema calcula automáticamente el total de cada pedido.

## Tecnologías Utilizadas

- Lenguaje de Programación: *[Java, Python]*
- IDE: *[IntelliJ, PyCharm]*
- Herramienta de Modelado UML: *[Visual Paradigm]*

## Instalación y Configuración

1. Clone el repositorio:
   git clone https://github.com/Jos748gran/MenuBoard.git