from django.urls import path
from . import views
from .views import index,crear_producto,subir_imagenes,detalle_producto,lista_productos,about,contacto
from .views import ver_favoritos, agregar_a_favoritos, eliminar_de_favoritos, actualizar_favoritos
from .views import custom_login, register, profile_view, logout_view, ProfileUpdateView
from .views import custom_password_reset_request, CustomPasswordResetDoneView, CustomPasswordResetConfirmView, CustomPasswordResetCompleteView


urlpatterns = [
    
     # Rutas para las vistas generales
    path('', index, name='index'),  # URL para ver la lista de productos
    path('about/', about, name='about'),  # URL para ver la lista de productos
    path('contacto/', contacto, name='contacto'),  # URL para ver la lista de productos
    
    
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
    
    
    path('shop/', views.shop, name='shop'),  # URL para ver la lista de productos
    
    
    
    path('producto/editar/<slug:slug>/', views.editar_producto, name='editar_producto'),
    path('producto/modificar_imagenes/<slug:slug>/', views.modificar_imagenes, name='modificar_imagenes'),
    path('producto/eliminar_imagen/<int:imagen_id>/', views.eliminar_imagen, name='eliminar_imagen'),
    
    path('producto/<slug:slug>/opinion/', views.dejar_opinion, name='producto_opinion'),
    
    
    path('favoritos/', ver_favoritos, name='ver_favoritos'),
    path('favoritos/agregar/<slug:slug>/', agregar_a_favoritos, name='agregar_a_favoritos'),
    path('favoritos/eliminar/<slug:slug>/', eliminar_de_favoritos, name='eliminar_de_favoritos'),
    path('favoritos/actualizar/<slug:slug>/', actualizar_favoritos, name='actualizar_favoritos'),
    
    
    path('editar-perfil/', ProfileUpdateView.as_view(), name='edit_profile'),
    #path('registro_exitoso/', registro_exitoso, name='registro_exitoso'),
    path('logout/', logout_view, name='logout'),
     path('login/', custom_login, name='login'),
    path('registro/', register, name='register'),
    path('profile/', profile_view, name='profile'),
    
    #####terminoos####
     path('terminos/', views.terminos, name='terminos'),  # URL para los términos
     path('terminos-condiciones/', views.terminos_condiciones, name='terminos_condiciones'),
    path('politica-privacidad/', views.politica_privacidad, name='politica_privacidad'),
    path('terminos-rembolso/', views.terminos_rembolso, name='terminos_rembolso'),
    
    path('password_reset/', custom_password_reset_request, name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    
]