
from django import forms
from django.core.exceptions import ValidationError
from .models import Categoria,Tag, Ingrediente,Producto,ProductoImagen

# Formulario para crear o editar una categoría
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']
        
    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        # Verificar si el color ya está registrado
        if Categoria.objects.filter(nombre=nombre).exists():
            raise forms.ValidationError(f'la Categoria "{nombre}" ya está registrado.')
        return nombre.title()


class IngredienteForm(forms.ModelForm):
    class Meta:
        model = Ingrediente
        fields = ['nombre']
        
    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        # Verificar si el color ya está registrado
        if Ingrediente.objects.filter(nombre=nombre).exists():
            raise forms.ValidationError(f'El Ingrediente "{nombre}" ya está registrado.')
        return nombre.title() 
    
class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['nombre']

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        # Verificar si el color ya está registrado
        if Tag.objects.filter(nombre=nombre).exists():
            raise forms.ValidationError(f'El Tag "{nombre}" ya está registrado.')
        return nombre.title()
    
    
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'sku', 'nombre', 'marca', 'descripcion', 'instrucciones',
            'presentacion', 'precio', 'descuento', 'categoria',
            'tags', 'ingredientes', 'activo'
        ]
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'instrucciones': forms.Textarea(attrs={'rows': 3}),
            'tags': forms.CheckboxSelectMultiple(),
            'ingredientes': forms.CheckboxSelectMultiple(),
            'categoria': forms.Select()
        }

    def clean_descuento(self):
        descuento = self.cleaned_data.get('descuento')
        if descuento < 0 or descuento > 100:
            raise forms.ValidationError("El descuento debe estar entre 0 y 100.")
        return descuento
    
    
class ProductoImagenForm(forms.ModelForm):
    class Meta:
        model = ProductoImagen
        fields = ['imagen']

    def __init__(self, *args, **kwargs):
        super(ProductoImagenForm, self).__init__(*args, **kwargs)
        producto = kwargs.get('instance').producto if 'instance' in kwargs else None
        if producto:
            self.fields['producto'].initial = producto
    