from django.db import models
from django.contrib.auth.models import User
from web.models import Producto


# ---------------------
# Carrito y Items
# ---------------------
class Carrito(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    creado = models.DateTimeField(auto_now_add=True)

    @property
    def total(self):
        return sum(item.subtotal() for item in self.items.all())

    def __str__(self):
        return f"Carrito {self.id} - Usuario: {self.usuario.username}"


class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.producto.precio * self.cantidad

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"


# ---------------------
# Pedido (dirección de envío)
# ---------------------
class Pedido(models.Model):
    carrito = models.OneToOneField(Carrito, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Usuario obligatorio
    nombre_completo = models.CharField(max_length=100)
    direccion = models.TextField()
    ciudad = models.CharField(max_length=50)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    creado = models.DateTimeField(auto_now_add=True)
    completado = models.BooleanField(default=False)

    def __str__(self):
        return f"Pedido {self.id} - {self.usuario.username}"


# ---------------------
# Pago
# ---------------------
class Pago(models.Model):
    ESTADO_CHOICES = (
        ('pendiente', 'Pendiente'),
        ('confirmado', 'Confirmado'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Usuario obligatorio
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pago {self.id} - {self.estado}"


# ---------------------
# Venta y Líneas de Venta
# ---------------------
class Venta(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Usuario obligatorio
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pago = models.OneToOneField(Pago, null=True, blank=True, on_delete=models.SET_NULL)
    envio = models.CharField(
        max_length=20,
        choices=[('envio', 'Envío a domicilio'), ('retiro', 'Retiro en tienda')],
        default='envio'
    )

    def calcular_total(self):
        self.total = sum(linea.subtotal() for linea in self.lineas.all())
        self.save()

    def __str__(self):
        return f"Venta {self.id} - Usuario: {self.user.username}"


class LineaVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='lineas')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f"{self.producto.nombre} - {self.cantidad} unidades"

    @property
    def total_formateado(self):
        return f"{self.subtotal():,.2f}"
