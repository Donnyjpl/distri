from django.urls import path
from . import views

urlpatterns = [
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<slug:slug>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('actualizar_envio/', views.actualizar_envio, name='actualizar_envio'),
    path('carrito/eliminar/<slug:slug>/', views.eliminar_del_carrito, name='eliminar_producto_carrito'),
    path('carrito/actualizar/<slug:slug>/', views.actualizar_cantidad_carrito, name='actualizar_producto_simple'),
]
