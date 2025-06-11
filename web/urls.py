from django.urls import path
from . import views
from .views import categoria_create,index,crear_producto,subir_imagenes,detalle_producto,lista_productos

urlpatterns = [
    
     # Rutas para las vistas generales
    path('', index, name='index'),  # URL para ver la lista de productos
    #path('about/', about, name='about'),  # URL para ver la lista de productos
    #path('contacto/', contacto, name='contacto'),  # URL para ver la lista de productos
    
    
    # Rutas para crear categorías y tags

    path('categorias/', views.categoria_list, name='categoria_list'),
    path('categorias/crear/', views.categoria_create, name='categoria_create'),
    path('categorias/editar/<int:pk>/', views.categoria_edit, name='categoria_edit'),
    path('categorias/eliminar/<int:pk>/', views.categoria_delete, name='categoria_delete'),
    
    path('tag/', views.tag_list, name='tag_list'),
    path('tag/crear/', views.tag_create, name='tag_create'),
    path('tag/editar/<int:pk>/', views.tag_edit, name='tag_edit'),
    path('tag/eliminar/<int:pk>/', views.tag_delete, name='tag_delete'),
    
    path('ingrediente/', views.ingrediente_list, name='ingrediente_list'),
    path('ingrediente/crear/', views.ingrediente_create, name='ingrediente_create'),
    path('ingrediente/editar/<int:pk>/', views.ingrediente_edit, name='ingrediente_edit'),
    path('ingrediente/eliminar/<int:pk>/', views.ingrediente_delete, name='ingrediente_delete'),
    
    path('producto/nuevo/',crear_producto , name='crear'),
    path('Producto/subir_imagenes/<slug:slug>/',subir_imagenes, name='subir_imagenes'),
    path('producto/<slug:slug>/', detalle_producto, name='detalle_producto'),
    path('producto/', lista_productos, name='listar'),  # URL para ver la lista de productos
    
    
    
    path('producto/editar/<slug:slug>/', views.editar_producto, name='editar_producto'),
    path('producto/modificar_imagenes/<slug:slug>/', views.modificar_imagenes, name='modificar_imagenes'),
    path('producto/eliminar_imagen/<int:imagen_id>/', views.eliminar_imagen, name='eliminar_imagen'),
    
    
]