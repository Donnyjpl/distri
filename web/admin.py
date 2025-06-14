from django.contrib import admin
from .models import Categoria, Tag, Ingrediente, Producto, ProductoImagen,OpinionCliente

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)
    
    
@admin.register(OpinionCliente)
class OpinionClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'producto', 'user', 'opinion', 'valoracion', 'created_at')
    search_fields = ('producto__nombre', 'user__username', 'opinion')
    list_filter = ('valoracion', 'created_at')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)

@admin.register(Ingrediente)
class IngredienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)

class ProductoImagenInline(admin.TabularInline):
    model = ProductoImagen
    extra = 1

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('sku', 'nombre', 'precio', 'descuento', 'activo', 'categoria')
    list_filter = ('categoria', 'activo')
    search_fields = ('nombre', 'sku')
    prepopulated_fields = {"slug": ("nombre",)}
    filter_horizontal = ('tags', 'ingredientes')
    inlines = [ProductoImagenInline]
# Register your models here.
