from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify  # Utilidad para crear el slug automáticamente
import uuid
from django.db import models
from django.utils.text import slugify

from decimal import Decimal  # Asegúrate de importar esto arriba del archivo


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dni = models.CharField(max_length=8,unique=True,
        null=True,
        blank=True,
        verbose_name="DNI"
    )
    
    telefono = models.CharField(
        max_length=15,
        unique=True,
        verbose_name="Teléfono"
    )
    
    direccion = models.CharField(max_length=255,verbose_name="Dirección")
    
    acepta_terminos = models.BooleanField(default=False,verbose_name="Acepta términos y condiciones")

    def __str__(self):
        return f"Perfil de {self.user.username}"
    


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Tag(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Ingrediente(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    sku = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(max_length=1000, null=True, blank=True)
    instrucciones = models.TextField(null=True, blank=True, help_text="Cómo consumir el producto")
    presentacion = models.CharField(max_length=255, null=True, blank=True, help_text="Ej: Botella de 600ml")
    precio = models.DecimalField(max_digits=10,decimal_places=2, help_text="Precio en soles (S/). Usa punto como separador decimal.")
    descuento = models.IntegerField(default=0, help_text="Porcentaje de descuento (0-100)")
    slug = models.SlugField(unique=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    ingredientes = models.ManyToManyField(Ingrediente, blank=True)
    activo = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug or (self.pk and self.sku != Producto.objects.get(pk=self.pk).sku):
            self.slug = slugify(self.sku)
        super().save(*args, **kwargs)
        
    @property
    def precio_formateado(self):
       return f"S/ {self.precio_con_descuento:,.2f}"
   
   
    @property
    def precio_con_descuento(self):
        if self.descuento:
            return self.precio * (Decimal(1) - Decimal(self.descuento) / Decimal(100))
        return self.precio

    @property
    def tiene_descuento(self):
        return self.descuento > 0

    def __str__(self):
        return f"{self.nombre} ({self.sku})"

class ProductoImagen(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='productos/')

    def __str__(self):
        return f"Imagen de {self.producto.nombre}"

    
class OpinionCliente(models.Model):
        producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='opiniones')
        user = models.ForeignKey(User, on_delete=models.CASCADE)  # opinion la venta con un usuario
        opinion = models.TextField()
        valoracion = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
        created_at = models.DateTimeField(auto_now_add=True)  # Campo para la fecha de creación

        def __str__(self):
            return f'Opinión de {self.user.username} sobre {self.producto.nombre}'  # Acceso al nombre del producto usando self.producto.name


class Contacto(models.Model):
    contact_form_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    customer_name = models.CharField(max_length=64)
    customer_email = models.EmailField()
    message = models.TextField()
    contacted = models.BooleanField(default=False)  # Campo para indicar si el mensaje ha sido contactado
    date_contacted = models.DateTimeField(null=True, blank=True)  # Fecha y hora en que se contactó al cliente 
  
    def __str__(self):
        return f"Formulario de Contacto - {self.contact_form_uuid}"
    

