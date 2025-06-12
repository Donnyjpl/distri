
from django import forms
from django.core.exceptions import ValidationError
from .models import Categoria,Tag, Ingrediente,Producto,ProductoImagen, OpinionCliente,Profile,Contacto
from django.contrib.auth.forms import SetPasswordForm,UserCreationForm
from django.contrib.auth.models import User
import re


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
            'sku', 'nombre', 'descripcion', 'instrucciones',
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
            
            
class ProductoFilterForm(forms.Form):
    nombre = forms.CharField(required=False, label='Buscar por nombre')
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        required=False,
        label='Categoría'
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Tags'
    )
    
    
class OpinionClienteForm(forms.ModelForm):
    class Meta:
        model = OpinionCliente
        fields = ['opinion', 'valoracion']
        widgets = {
            'opinion': forms.Textarea(attrs={'rows': 3, 'cols': 50}),
            
        }
        
        
class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = ['customer_name', 'customer_email', 'message']
        labels = {
            'customer_name': 'Nombre:',
            'customer_email': 'Correo Electrónico:',
            'message': 'Mensaje:',
        }
        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'form-control',  # Clase de Bootstrap
                'placeholder': 'Ingresa tu nombre',  # Placeholder
            }),
            'customer_email': forms.EmailInput(attrs={
                'class': 'form-control',  # Clase de Bootstrap
                'placeholder': 'Ingresa tu correo electrónico',  # Placeholder
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',  # Clase de Bootstrap
                'cols': 30,
                'rows': 3,
                'placeholder': 'Escribe tu mensaje aquí...',  # Placeholder
            }),
        }
 

class CustomPasswordResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="Nueva Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu nueva contraseña'}),
    )
    new_password2 = forms.CharField(
        label="Confirmar Nueva Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirma tu nueva contraseña'}),
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")

        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
    
    
class CustomEmailForm(forms.Form):
    email = forms.EmailField(
        label="Correo Electrónico",
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu correo electrónico'}),
    )
    
class LoginForm(forms.Form):
    username = forms.CharField(
        label='Nombre de usuario',
        widget=forms.TextInput(attrs={
            'class': 'form-control',  # Clase de Bootstrap
            'placeholder': 'Ingresa tu correo',  # Placeholder
        })
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',  # Clase de Bootstrap
            'placeholder': 'Ingresa tu contraseña',  # Placeholder
        })
    )
# Formulario para crear un usuario con campos adicionales
# Formulario para crear un usuario con campos adicionales

class CustomUserCreationForm(UserCreationForm):
    nombre = forms.CharField(max_length=30, required=True)
    apellido = forms.CharField(max_length=30, required=True)
    dni = forms.CharField(max_length=8, required=True, label="DNI")
    telefono = forms.CharField(max_length=15, required=True)
    direccion = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}), required=True)
    acepta_terminos = forms.BooleanField(
        required=True, 
        label="Acepto los términos y condiciones",
        error_messages={'required': 'Debes aceptar los términos y condiciones para registrarte.'}
    )

    class Meta:
        model = User
        fields = ['nombre', 'apellido', 'email', 'dni', 'password1', 'password2', 'telefono', 'direccion']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este correo electrónico ya está registrado.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Las contraseñas deben ser iguales.")

        if password1:
            if len(password1) < 8:
                raise ValidationError("La contraseña debe tener al menos 8 caracteres.")
            if password1.isdigit():
                raise ValidationError("La contraseña no puede ser completamente numérica.")

        return password2

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        # Asegúrate que Profile es importado y tiene el campo telefono
        if Profile.objects.filter(telefono=telefono).exists():
            raise ValidationError("Este número de teléfono ya está registrado.")
        return telefono

    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        # Validar que DNI tenga 7 u 8 dígitos y solo números
        if not re.fullmatch(r'\d{7,8}', dni):
            raise ValidationError("El DNI debe contener sólo números y tener 7 u 8 dígitos.")
        # Puedes agregar validación para que no exista en Profile si lo usas ahí
        if Profile.objects.filter(dni=dni).exists():
            raise ValidationError("Este DNI ya está registrado.")
        return dni

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['nombre']
        user.last_name = self.cleaned_data['apellido']
        user.username = self.cleaned_data['email']

        if commit:
            user.save()

        profile = Profile.objects.create(
            user=user,
            dni=self.cleaned_data['dni'],  # Cambié rut por dni aquí
            telefono=self.cleaned_data['telefono'],
            direccion=self.cleaned_data['direccion']
        )
        return user
# Formulario para crear o actualizar el perfil del usuario
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [ 'dni','telefono', 'direccion']
        