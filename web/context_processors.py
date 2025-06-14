from .models import Categoria
from compras.models import Carrito, ItemCarrito

def categorias_y_datos_adicionales(request):
    # Obtener categorías
    categorias = Categoria.objects.all()[:5]

    # Obtener cantidad del carrito desde DB si el usuario está autenticado
    cantidad_carrito = 0
    if request.user.is_authenticated:
        try:
            carrito = Carrito.objects.get(usuario=request.user)
            cantidad_carrito = sum(item.cantidad for item in carrito.items.all())
        except Carrito.DoesNotExist:
            pass
    else:
        # Carrito en sesión para usuarios anónimos
        carrito_sesion = request.session.get('carrito', {})
        cantidad_carrito = sum(
            item['cantidad'] for producto in carrito_sesion.values()
            for item in producto.get('tallas', {}).values()
        )

    # Favoritos desde sesión
    favoritos = request.session.get('favoritos', {})
    cantidad_favoritos = len(favoritos)

    return {
        'categorias': categorias,
        'cantidad_carrito': cantidad_carrito,
        'cantidad_favoritos': cantidad_favoritos,
    }
