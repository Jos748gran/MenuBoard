# MenuBoard

# Proyecto
MenuBoard es un sistema de gestión de restaurantes diseñado para facilitar la administración de restaurantes, cafeterías o cualquier establecimiento de alimentos y bebidas. La aplicación permite crear, modificar y gestionar menús de manera eficiente, proporcionando a los usuarios una interfaz sencilla para realizar actualizaciones rápidas, gestionar categorías de platos y actualizar precios de forma intuitiva.

## Descripción
MenuBoard es un proyecto orientado a simplificar la gestión de menús digitales. El sistema permite a los administradores agregar platos, organizar menús por categorías y modificar descripciones o precios de manera dinámica. El objetivo principal es ofrecer una herramienta que permita la actualización en tiempo real de los menús, brindando flexibilidad para adaptarse a cambios en los ingredientes, promociones o ajustes de precios.

## Funcionalidades

### Grupo 1: Módulo de Mesas y Reservaciones
Este módulo gestiona la disponibilidad y uso de las mesas dentro del restaurante. Las mesas pueden estar en diferentes estados, tales como libre, ocupada o reservada. Los clientes pueden hacer reservaciones de mesas con antelación, especificando la fecha y hora de la reserva. Es necesario gestionar las características de cada mesa, como el número de asientos y su ubicación en el restaurante. Cuando un cliente llega, una mesa puede ser asignada, y al finalizar su uso, la mesa debe ser liberada para otros clientes. Las reservaciones pueden ser modificadas o canceladas por el cliente o el personal del restaurante.

##### Requerimientos mínimos:
* Registrar la cantidad total de mesas en el restaurante, incluyendo atributos como identificación, número de asientos y ubicación.
* Permitir el cambio de estado de una mesa: libre, ocupada, reservada.
* Registrar nuevas reservaciones, especificando datos como nombre del cliente, cantidad de personas, fecha y hora.
* Modificar o cancelar reservaciones existentes.
* Asignar mesas a clientes que llegan sin reservación.
* Notificar al personal cuando una mesa está lista para ser asignada.
* Gestionar la lista de espera cuando todas las mesas estén ocupadas.
* Permitir la unión de varias mesas permitiendo que sean fusionadas temporalmente

### Grupo 2: Módulo de Pedidos
El módulo de pedidos permite gestionar los pedidos de los clientes, desde que se realiza el pedido hasta que es servido y pagado. Cada pedido puede contener uno o más productos del menú, y es posible agregar o eliminar productos mientras el pedido no haya sido servido. El sistema debe permitir modificar cantidades de productos en los pedidos, así como su estado (pendiente, en preparación, servido, pagado). El personal del restaurante puede visualizar y actualizar el estado de cada pedido. Además, se requiere tener un registro histórico de todos los pedidos realizados en el restaurante para futuras consultas.

##### Requerimientos:
* Crear un nuevo pedido asociándolo a una mesa o a una reservación.
* Agregar productos al pedido, especificando cantidad y detalles del producto.
* Modificar los productos dentro del pedido (cambiar cantidades, eliminar productos).
* Cambiar el estado del pedido: pendiente, en preparación, servido, pagado.
* Permitir la visualización de los pedidos por parte del personal de cocina, mostrando detalles como mesa, productos y estado.
* Registrar un historial de todos los pedidos realizados, incluyendo fecha, mesa, cliente y monto total.
* Generar un resumen del pedido para ser entregado a la cocina.

### Grupo 3: Módulo de Menús y Productos
Este módulo permite gestionar los productos y platos que se ofrecen en el restaurante. Cada producto tiene atributos como nombre, descripción, categoría, precio y disponibilidad. El menú puede estar organizado en categorías, como entradas, platos principales, postres y bebidas. El sistema debe permitir agregar nuevos productos al menú, modificarlos o eliminarlos cuando sea necesario. Además, se requiere que los productos puedan estar temporalmente fuera de stock o deshabilitados para su venta si los ingredientes no están disponibles. También se debe mantener un control de precios, permitiendo actualizarlos según sea necesario.

##### Requerimientos:
* Crear nuevos productos para el menú, con información detallada como nombre, descripción, categoría, precio y disponibilidad.
* Clasificar productos en diferentes categorías (entradas, platos principales, postres, bebidas).
* Modificar los atributos de los productos existentes, incluyendo descripción y precio.
* Marcar productos como disponibles o no disponibles según el inventario.
* Visualizar el menú completo, permitiendo filtrar por categoría y disponibilidad.
* Registrar los cambios en los productos para efectos de control interno.

### Grupo 4: Módulo de Facturación y Pagos
Este módulo es responsable de generar la factura para los clientes al finalizar su pedido. La factura debe calcular automáticamente el total del pedido, incluyendo impuestos y descuentos aplicables. Además, debe permitir seleccionar el método de pago, ya sea en efectivo, tarjeta de crédito o débito, entre otros. El sistema debe generar un comprobante de pago que puede ser impreso o enviado al correo del cliente. También es necesario mantener un registro de todas las facturas emitidas para efectos contables y de auditoría.

##### Requerimientos:
* Generar una factura detallada al finalizar el pedido, con información como productos, cantidades, precios, impuestos y total.
* Aplicar descuentos si es necesario y recalcular el total de la factura.
* Registrar diferentes métodos de pago, como efectivo, tarjeta de crédito o transferencia bancaria.
* Generar un comprobante de pago para ser entregado al cliente, ya sea impreso o por correo electrónico.
* Mantener un registro histórico de todas las facturas emitidas, permitiendo la consulta por fecha, cliente o monto.
* Integrar el sistema de facturación con el módulo de pedidos para facilitar el proceso de pago.
* Integrar promociones

### Grupo 5: Módulo de Inventario
El módulo de inventario permite gestionar los insumos y productos necesarios para la preparación de los platos del restaurante. Cada insumo debe ser registrado con información como nombre, cantidad disponible y unidad de medida. El sistema debe permitir registrar entradas de nuevos insumos y salidas de los mismos cuando se utilizan en la preparación de los productos del menú. Además, es necesario generar alertas cuando el inventario de un insumo esté bajo o agotado. También debe permitir generar reportes de consumo de insumos y de stock disponible para facilitar la reposición.

##### Requerimientos:
* Registrar todos los insumos del restaurante, con información como nombre, cantidad, unidad de medida y nivel de reorden.
* Permitir registrar entradas al inventario (compras de insumos) y salidas del inventario (uso de insumos).
* Actualizar en tiempo real la cantidad disponible de cada insumo según el uso en los pedidos.
* Generar alertas automáticas cuando la cantidad de un insumo está por debajo del nivel de reorden.
* Generar reportes sobre el consumo de insumos en un período determinado, permitiendo identificar los más utilizados.
* Mantener un historial de las entradas y salidas para fines de auditoría y control.

### Grupo 6: Módulo de Reportes y Estadísticas
Este módulo proporciona información sobre el desempeño del restaurante a través de reportes y estadísticas. Los reportes incluyen datos sobre las ventas diarias, productos más vendidos, mesas más utilizadas, ingresos generados, y el desempeño de los empleados. El sistema debe permitir generar reportes personalizados por rango de fechas y categorías específicas, como ventas por categoría de producto o por empleado. Además, se deben generar gráficos y tablas que faciliten la interpretación de los datos.

##### Requerimientos:
* Generar reportes de ventas diarias, semanales y mensuales, desglosando por productos y categorías.
* Mostrar estadísticas sobre los productos más vendidos y las mesas más utilizadas en el restaurante.
* Generar reportes personalizados según el rango de fechas y las categorías solicitadas.
* Producir gráficos visuales que resuman el rendimiento del restaurante, facilitando la interpretación de datos.
* Permitir guardar los reportes en formatos digitales (PDF, Excel) para su uso posterior.
* Mostrar el rendimiento de los empleados en términos de ventas y pedidos atendidos.