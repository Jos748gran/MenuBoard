from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
from util import views as util_views
from pedidos import views as pedidos_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', util_views.home, name="home"),
    path('user/', util_views.user, name="user"),
    path('staff/',util_views.staff, name="staff"),
    path('login/', util_views.login_view, name='login'),
    path('register/', util_views.register_view, name='register'),
    path('pedidos/', util_views.pedidos, name='pedidos'),
    path('menus/', util_views.menus, name='menus'),
    path('mesas/', util_views.mesas, name='mesas'),
    path('clientes/', util_views.clientes, name='clientes'),
    path('meseros/', util_views.meseros, name='meseros'),
    path('personal_cocina/', util_views.personal_cocina, name='personal_cocina'),
    path('crear_plato/', pedidos_views.crear_plato, name='crear_plato'),
    path('modificar_plato/<int:id>/', pedidos_views.modificar_plato, name='modificar_plato'),
    path('eliminar_plato/<int:id>/', pedidos_views.eliminar_plato, name='eliminar_plato'),
    path('crear_mesa/', pedidos_views.crear_mesa, name='crear_mesa'),
    path('modificar_mesa/<int:id>/', pedidos_views.modificar_mesa, name='modificar_mesa'),
    path('eliminar_mesa/<int:id>/', pedidos_views.eliminar_mesa, name='eliminar_mesa'),
    path('crear_cliente/', pedidos_views.crear_cliente, name='crear_cliente'),
    path('modificar_cliente/<int:id>/', pedidos_views.modificar_cliente, name='modificar_cliente'),
    path('eliminar_cliente/<int:id>/', pedidos_views.eliminar_cliente, name='eliminar_cliente'),
    path('crear_pedido/', pedidos_views.crear_pedido, name='crear_pedido'),
    path('modificar_pedido/<int:id>/', pedidos_views.modificar_pedido, name='modificar_pedido'),
    path('eliminar_pedido/<int:id>/', pedidos_views.eliminar_pedido, name='eliminar_pedido'),
    path('crear_mesero/', pedidos_views.crear_mesero, name='crear_mesero'),
    path('modificar_mesero/<int:id>/', pedidos_views.modificar_mesero, name='modificar_mesero'),
    path('eliminar_mesero/<int:id>/', pedidos_views.eliminar_mesero, name='eliminar_mesero'),
    path('crear_personal_cocina/', pedidos_views.crear_personal_cocina, name='crear_personal_cocina'),
    path('modificar_personal_cocina/<int:id>/', pedidos_views.modificar_personal_cocina, name='modificar_personal_cocina'),
    path('eliminar_personal_cocina/<int:id>/', pedidos_views.eliminar_personal_cocina, name='eliminar_personal_cocina'),
    path('crear_item_pedido/', pedidos_views.crear_item_pedido, name='crear_item_pedido'),
    path('modificar_item_pedido/<int:id>/', pedidos_views.modificar_item_pedido, name='modificar_item_pedido'),
    path('eliminar_item_pedido/<int:id>/', pedidos_views.eliminar_item_pedido, name='eliminar_item_pedido'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
