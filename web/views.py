from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Categoria, Tag, Ingrediente,Producto,ProductoImagen,OpinionCliente,Profile
from .forms import CategoriaForm, TagForm, IngredienteForm,ProductoForm, ProductoImagenForm,ProductoFilterForm,OpinionClienteForm,ContactoForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin       
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User             
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout                      
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView
from django.core.mail import send_mail
from django.conf import settings
from .forms import CustomUserCreationForm, LoginForm



from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, ListView, DetailView, View
from django.views.generic.edit import UpdateView
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy, reverse
from django.db.models import Avg, Prefetch
from django.utils import timezone
from django.core.paginator import Paginator
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes, smart_str
from django.db.models import Prefetch
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django import forms

def pagina_no_encontrada(request, exception):
    return render(request, '404.html', status=404)

def es_superusuario(user):
    return user.is_superuser

# crud de categorias
@user_passes_test(es_superusuario)
def categoria_create(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categoria_list')
    else:
        form = CategoriaForm()
    return render(request, 'categoria/categoria_form.html', {'form': form})

@user_passes_test(es_superusuario)
def categoria_list(request):
    categorias = Categoria.objects.all()
    return render(request, 'categoria/categoria_list.html', {'categorias': categorias})

@user_passes_test(es_superusuario)
def categoria_delete(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        return redirect('categoria_list')
  
    return render(request, 'categoria/categoria_confirm_delete.html', {'categoria': categoria})
@user_passes_test(es_superusuario)
def categoria_edit(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('categoria_list')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'categoria/categoria_form.html', {'form': form})


# crud de tags
@user_passes_test(es_superusuario)
def tag_create(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tag_list')
    else:
        form = TagForm()
    return render(request, 'tag/tag_form.html', {'form': form})

@user_passes_test(es_superusuario)
def tag_list(request):
    tags= Tag.objects.all()
    return render(request, 'tag/tag_list.html', {'tags': tags})

@user_passes_test(es_superusuario)
def tag_delete(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    if request.method == 'POST':
        tag.delete()
        return redirect('tag_list')
    return render(request, 'tag/tag_confirm_delete.html', {'tag': tag})

@user_passes_test(es_superusuario)
def tag_edit(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    if request.method == 'POST':
        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            return redirect('tag_list')
    else:
        form = TagForm(instance=tag)
    return render(request, 'tag/tag_form.html', {'form': form})


# crud de ingredientes
@user_passes_test(es_superusuario)
def ingrediente_create(request):
    if request.method == 'POST':
        form = IngredienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ingrediente_list')
    else:
        form = TagForm()
    return render(request, 'ingrediente/ingrediente_form.html', {'form': form})

@user_passes_test(es_superusuario)
def ingrediente_list(request):
    ingredientes= Ingrediente.objects.all()
    return render(request, 'ingrediente/ingrediente_list.html', {'ingredientes': ingredientes})

@user_passes_test(es_superusuario)
def ingrediente_delete(request, pk):
    ingrediente = get_object_or_404(Ingrediente, pk=pk)
    if request.method == 'POST':
        ingrediente.delete()
        return redirect('ingrediente_list')
    return render(request, 'ingrediente/ingrediente_confirm_delete.html', {'ingrediente': ingrediente})

@user_passes_test(es_superusuario)
def ingrediente_edit(request, pk):
    ingrediente = get_object_or_404(Ingrediente, pk=pk)
    if request.method == 'POST':
        form = TagForm(request.POST, instance=ingrediente)
        if form.is_valid():
            form.save()
            return redirect('ingrediente_list')
    else:
        form = TagForm(instance=ingrediente)
    return render(request, 'ingrediente/ingrediente_form.html', {'form': form})


@user_passes_test(es_superusuario)
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save()  # Guardar el producto
            messages.success(request, f'Producto {producto.nombre} creado exitosamente.')
            return redirect('subir_imagenes', slug=producto.slug)
    else:
        form = ProductoForm()
    return render(request, 'productos/crear_producto.html', {'form': form})

@user_passes_test(es_superusuario)
def subir_imagenes(request, slug):
    producto = get_object_or_404(Producto, slug=slug)  # Buscar producto por slug
    if request.method == 'POST':
        # Validar si ya se alcanzó el límite de imágenes
        if producto.imagenes.count() >= 5:
            messages.warning(request, 'Ya has subido el máximo de 5 imágenes para este producto.')
            return redirect('detalle_producto', slug=producto.slug)  # O redirige a donde prefieras

        form = ProductoImagenForm(request.POST, request.FILES)
        if form.is_valid():
            imagen = form.save(commit=False)
            imagen.producto = producto
            imagen.save()
            messages.success(request, 'Imagen subida exitosamente.')

            if producto.imagenes.count() >= 5:
                messages.success(request, 'Se han subido todas las imágenes. Proceso completo.')
                return redirect('detalle_producto', slug=producto.slug)
            else:
                restantes = 5 - producto.imagenes.count()
                messages.info(request, f'Te quedan {restantes} imagen(es) por subir.')
                return redirect('subir_imagenes', slug=producto.slug)
    else:
        form = ProductoImagenForm()

    return render(request, 'productos/subir_imagenes.html', {
        'form': form,
        'producto': producto
    })
    
    
    
def detalle_producto(request, slug):
    producto = get_object_or_404(Producto, slug=slug)

    relacionados = Producto.objects.filter(
        Q(categoria=producto.categoria) |
        Q(tags__in=producto.tags.all()),
        activo=True
    ).exclude(id=producto.id).distinct()[:4]

    return render(request, 'productos/detalle_producto.html', {
        'producto': producto,
        'productos_relacionados': relacionados
    })

@user_passes_test(es_superusuario)
def editar_producto(request, slug):
    producto = get_object_or_404(Producto, slug=slug)  # Obtener el producto a editar por su slug

    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)  # Inicializamos el formulario con los datos del producto
        if form.is_valid():
            form.save()  # Guardamos los cambios en el producto
            messages.success(request, f'Producto {producto.nombre} actualizado exitosamente.')
            return redirect('detalle_producto', slug=producto.slug)  # Redirigimos a los detalles del producto
    else:
        form = ProductoForm(instance=producto)  # En GET, prellenamos el formulario con el producto existente

    return render(request, 'productos/editar_producto.html', {'form': form, 'producto': producto})


@user_passes_test(es_superusuario)
def modificar_imagenes(request, slug):
    producto = get_object_or_404(Producto, slug=slug)
    imagenes = producto.imagenes.all()  # Obtener las imágenes existentes
    
    if imagenes.count() >= 5:  # Corregir a `count()`
        # Limitar la cantidad de fotos a 5
        messages.warning(request, 'Ya no puedes agregar más de 5 fotos.')
        return render(request, 'productos/modificar_imagenes.html', {'producto': producto, 'imagenes': imagenes})
    
    # Asegurarse de que el formulario siempre esté presente, incluso para una solicitud GET
    form = ProductoImagenForm()

    if request.method == 'POST':
        form = ProductoImagenForm(request.POST, request.FILES)
        if form.is_valid():
            imagen = form.save(commit=False)
            imagen.producto = producto  # Asignar la imagen al producto
            imagen.save()
            messages.success(request, 'Imagen modificada exitosamente.')
            return redirect('modificar_imagenes', slug=producto.slug)
    
    return render(request, 'productos/modificar_imagenes.html', {'form': form, 'producto': producto, 'imagenes': imagenes})


@user_passes_test(es_superusuario)
def eliminar_imagen(request, imagen_id):
    # Obtener la imagen por su ID
    imagen = get_object_or_404(ProductoImagen, id=imagen_id)

    # Guardar el producto relacionado
    producto_slug = imagen.producto.slug

    # Eliminar la imagen
    imagen.delete()

    # Mensaje de éxito
    messages.success(request, 'Imagen eliminada exitosamente.')

    # Redirigir al usuario a la página de modificación de imágenes del producto
    return redirect('modificar_imagenes', slug=producto_slug)

@user_passes_test(es_superusuario)
def lista_productos(request):
    # Obtener todos los productos activos
    productos = Producto.objects.filter(activo=True).order_by('nombre').prefetch_related('imagenes')

    # Si tienes un formulario de filtro, puedes integrarlo aquí:
    # form = ProductoFilterForm(request.GET)
    # if form.is_valid():
    #     # Aplica filtros al queryset productos según los datos del formulario
    #     productos = form.filtrar(productos)  # ejemplo, debes implementar filtrar()

    # Paginación: 10 productos por página
    paginator = Paginator(productos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'productos/producto_list.html', {
        'page_obj': page_obj,
        # 'form': form,  # Descomenta si usas filtro
    })
      
class ProductoListView(ListView):
    model = Producto
    template_name = 'shop.html'
    context_object_name = 'productos'
    paginate_by = 30

    def get_queryset(self):
        queryset = Producto.objects.filter(activo=True).order_by('nombre')
        queryset = queryset.prefetch_related('imagenes', 'tags', 'categoria')

        form = ProductoFilterForm(self.request.GET)
        if form.is_valid():
            nombre = form.cleaned_data.get('nombre')
            categoria = form.cleaned_data.get('categoria')
            tags = form.cleaned_data.get('tags')

            if nombre:
                queryset = queryset.filter(nombre__icontains=nombre)
            if categoria:
                queryset = queryset.filter(categoria=categoria)
            if tags:
                for tag in tags:
                    queryset = queryset.filter(tags=tag)

        order_by = self.request.GET.get('order_by', 'nombre')
        if order_by == 'name':
            queryset = queryset.order_by('nombre')
        elif order_by == 'item':
            queryset = queryset.order_by('slug')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ProductoFilterForm(self.request.GET)
        context['rango_estrellas'] = range(1, 6)
        return context
    
    
    
    #####favoritos
def agregar_a_favoritos(request, slug):
    # Obtener el producto usando el slug
    producto = get_object_or_404(Producto, slug=slug)
    
    # Obtener las imágenes del producto (tomamos la primera imagen disponible)
    imagen_producto = producto.imagenes.first()  # Si no hay imagen, será None
    
    # Obtener los favoritos de la sesión o inicializarlo si no existe
    favoritos = request.session.get('favoritos', {})

    # Verificar si el producto ya está en favoritos
    if str(slug) not in favoritos:
        favoritos[str(slug)] = {
            'nombre': producto.nombre,
            'precio': str(producto.precio),
            'slug': producto.slug,
            'imagen': imagen_producto.imagen.url if imagen_producto else None,  # Usar la URL de la imagen
        }
        # Guardar los favoritos en la sesión
        request.session['favoritos'] = favoritos
        messages.success(request, f'{producto.nombre} ha sido agregado a tus favoritos.')
    else:
        messages.info(request, f'{producto.nombre} ya está en tus favoritos.')

    return redirect('detalle_producto', slug=slug)  # Redirige a la página del producto

@login_required
def ver_favoritos(request):
    favoritos = request.session.get('favoritos', {})
    return render(request, 'favoritos/favoritos.html', {'favoritos': favoritos})
@login_required
def eliminar_de_favoritos(request, slug):
    # Obtener los favoritos de la sesión
    favoritos = request.session.get('favoritos', {})

    # Eliminar el producto de los favoritos
    if str(slug) in favoritos:
        del favoritos[str(slug)]
        request.session['favoritos'] = favoritos
        messages.success(request, f'Producto {slug} ha sido eliminado de tus favoritos.')
    else:
        messages.error(request, 'Producto no encontrado en tus favoritos.')

    return redirect('ver_favoritos')  # Redirige a la vista de favoritos

def actualizar_favoritos(request, slug):
    # Obtener los favoritos de la sesión
    favoritos = request.session.get('favoritos', {})

    # Si el producto está en los favoritos
    if str(slug) in favoritos:
        # Aquí puedes actualizar detalles adicionales si lo necesitas
        # Por ejemplo, puedes agregar un campo de "comentarios" o algo similar
        favoritos[str(slug)]['comentarios'] = request.POST.get('comentarios', '')
        request.session['favoritos'] = favoritos
        messages.success(request, 'Favoritos actualizados correctamente.')
    else:
        messages.error(request, 'Producto no encontrado en tus favoritos.')

    return redirect('ver_favoritos')  # Redirige a la vista de favoritos

@login_required    
def dejar_opinion(request, slug):
    producto = get_object_or_404(Producto, slug=slug)  # Obtener el producto por su slug

    if request.method == 'POST':
        form = OpinionClienteForm(request.POST)
        if form.is_valid():
            # Asignar el producto y el usuario a la opinión
            opinion = form.save(commit=False)
            opinion.producto = producto  # Asociar la opinión con el producto
            opinion.user = request.user  # Asignar el usuario autenticado
            opinion.save()  # Guardar la opinión

            # Mensaje de éxito
            messages.success(request, '¡Gracias por tu opinión!')
            return redirect('detalle_producto', slug=producto.slug)  # Redirigir a la página del producto
    else:
        form = OpinionClienteForm()

    return render(request, 'productos/dejar_opinion.html', {
        'form': form,
        'producto': producto
    })
    
    
def about(request):
    return render(request, 'about.html')

def contacto(request):
    return render(request, 'about.html')
def index(request):
    return render(request, 'index.html')


def terminos(request):
    return render(request, 'politicas/politicas.html')

def terminos_condiciones(request):
    return render(request, 'politicas/terminos_condiciones.html')

def politica_privacidad(request):
    return render(request, 'politicas/terminos_privacidad.html')

def terminos_rembolso(request):
    return render(request, 'politicas/terminos_rembolso.html')

def custom_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():

            # Recuperar los datos del formulario
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # Intentar autenticar al usuario
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'¡Bienvenido de nuevo, {user.username}!')
                return redirect('index')  # Redirige después de login exitoso
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')  # Mensaje de error
        else:
            messages.error(request, 'Formulario inválido')  # En caso de que el formulario no sea válido
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})



class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ['telefono', 'direccion']
    template_name = 'usuario/edit_profile.html'
    success_url = reverse_lazy('profile')  # Redirige al perfil después de la actualización
    
    def get_object(self, queryset=None):
        """
        Obtiene el perfil del usuario logueado.
        Si el perfil no existe, lo crea.
        """
        try:
            return self.request.user.profile
        except Profile.DoesNotExist:
            # Si no existe el perfil, lo creamos y lo asociamos al usuario
            profile = Profile.objects.create(user=self.request.user)
            return profile

    def get_form(self, form_class=None):
        """
        Sobrescribimos este método para incluir los campos adicionales del usuario (nombre, apellido, correo, direccion).
        """
        form = super().get_form(form_class)
        
        # Añadir los campos del User al formulario de actualización
        form.fields['username'] = forms.CharField(max_length=150)
        form.fields['email'] = forms.EmailField()
        form.fields['first_name'] = forms.CharField(max_length=30)
        form.fields['last_name'] = forms.CharField(max_length=30)
        
        # Campo dirección con tamaño personalizado (más grande)
        form.fields['direccion'] = forms.CharField(
            widget=forms.Textarea(attrs={'rows': 5, 'cols': 40})  # Cambié el tamaño del TextArea
        )

        # Inicializamos los valores de los campos con los valores del usuario logueado
        form.initial['username'] = self.request.user.username
        form.initial['email'] = self.request.user.email
        form.initial['first_name'] = self.request.user.first_name
        form.initial['last_name'] = self.request.user.last_name
        form.initial['direccion'] = self.request.user.profile.direccion  # Inicializamos direccion desde el perfil

        return form

    def form_valid(self, form):
        """
        Sobrescribimos este método para guardar los datos del User además de los del Profile.
        """
        user = self.request.user
        # Validar que el email no esté registrado
        email = form.cleaned_data['email']
        if User.objects.filter(email=email).exclude(username=user.username).exists():
            form.add_error('email', 'Este correo electrónico ya está registrado.')
            return self.form_invalid(form)

        # Validar que el teléfono no esté registrado
        telefono = form.cleaned_data['telefono']
        if Profile.objects.filter(telefono=telefono).exclude(user=user).exists():
            form.add_error('telefono', 'Este número de teléfono ya está registrado.')
            return self.form_invalid(form)

        # Guardar los campos de usuario
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.email = email  # Asignar el email
        user.username = email  # Establecer el username como email si es necesario
        user.save()

        # Guardar los campos de perfil
        profile = form.save(commit=False)
        profile.user = user  # Asegurarse de que el perfil está vinculado al usuario
        profile.direccion = form.cleaned_data['direccion']  # Guardamos la dirección también
        profile.save()

        # Agregar un mensaje de éxito después de guardar los cambios
        messages.success(self.request, '¡Perfil actualizado correctamente!')

        return super().form_valid(form)
    

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            # Verificamos que el usuario haya aceptado los términos
            if form.cleaned_data['acepta_terminos']:
                user = form.save()
                messages.success(request, '¡Cuenta registrada con éxito!')
                return redirect('login')  # Redirige a la página de inicio de sesión
            else:
                messages.error(request, 'Debes aceptar los términos y condiciones.')
        else:
            messages.error(request, 'Hubo un error en el registro. Por favor, corrige los errores.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})



def logout_view(request): # Cierra la sesión
    logout(request)  # Esto cierra la sesión del usuario
    return redirect('index')  # Redirige a la página de inicio o a la página que desees


# Vista personalizada para solicitar el restablecimiento de contraseña
def custom_password_reset_request(request):
    if request.method == "POST":
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            # Generar UID y token para el restablecimiento de contraseña
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            domain = request.get_host()
            reset_link = f"http://{domain}{reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})}"

            # Enviar el correo con el enlace de restablecimiento
            subject = "Restablecimiento de contraseña"
            message = f"""Hola {user.username},
Hemos recibido una solicitud para restablecer tu contraseña. Si no realizaste esta solicitud, puedes ignorar este correo.

Para restablecer tu contraseña, haz clic en el siguiente enlace:
<a href="{reset_link}">Restablecer contraseña</a>

Este enlace es válido solo por 24 horas.

Gracias,
Tu equipo"""

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
                html_message=message
            )
            
            return render(request, 'registration/password_reset_done.html')
        else:
            error_message = "No se encontró un usuario con ese correo electrónico."
            return render(request, 'registration/password_reset_form.html', {'error_message': error_message})

    return render(request, 'registration/password_reset_form.html')


# Vista personalizada para confirmar el restablecimiento de contraseña
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['custom_message'] = "¡Tu contraseña ha sido restablecida con éxito!"
        return context

# Usamos las vistas por defecto para las siguientes dos etapas
class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'

    
@login_required
def profile_view(request):
    return render(request, 'usuario/profile.html')



def contacto(request):
    if request.method == 'POST':
        formm = ContactoForm(request.POST)
        if formm.is_valid():
            # Guarda el formulario en la base de datos si es necesario
            formm.save()  # Este paso es opcional dependiendo de si deseas almacenar los datos

            # Obtener los datos del formulario
            nombre = formm.cleaned_data['customer_name']
            correo = formm.cleaned_data['customer_email']
            mensaje = formm.cleaned_data['message']
            
            # Crear el correo en formato texto plano y HTML para el administrador
            subject = f'Nuevo mensaje de contacto de {nombre}'
            from_email = correo
            to_email = ['info@tbkdesire.cl']  # Reemplaza con el correo del administrador

            # Texto plano para el correo
            text_content = f'Nuevo mensaje de contacto de {nombre}\n\nCorreo: {correo}\n\nMensaje:\n{mensaje}'
            
            # HTML para el correo
            html_content = f"""
                <html>
                    <body>
                        <h2>Nuevo mensaje de contacto de {nombre}</h2>
                        <p><strong>Correo:</strong> {correo}</p>
                        <p><strong>Mensaje:</strong></p>
                        <p>{mensaje}</p>
                    </body>
                </html>
            """
            
            # Crear el objeto de correo con texto plano y HTML
            email = EmailMultiAlternatives(
                subject,
                text_content,
                from_email,
                to_email,
            )
            
            # Adjuntar el contenido HTML al correo
            email.attach_alternative(html_content, "text/html")

            # Enviar el correo al administrador
            email.send(fail_silently=False)

            # Si también deseas enviar un correo al usuario de confirmación
            user_subject = f'Gracias por tu mensaje, {nombre}'
            user_message = f"""
                <html>
                    <body>
                        <h2>Gracias por ponerte en contacto con nosotros, {nombre}!</h2>
                        <p>Hemos recibido tu mensaje y nos pondremos en contacto contigo pronto.</p>
                        <p><strong>Tu mensaje:</strong></p>
                        <p>{mensaje}</p>
                    </body>
                </html>
            """
            user_email = EmailMultiAlternatives(
                user_subject,
                user_message, 
                'info@tbkdesire.cl',  # Dirección del remitente (puedes cambiarla)
                [correo]
            )

            # Adjuntar el contenido HTML al correo del usuario
            user_email.attach_alternative(user_message, "text/html")
            user_email.send(fail_silently=False)

            # Mensaje de éxito para el usuario
            messages.success(request, 'Tu mensaje ha sido enviado al administrador. ¡Gracias!')

            # Redirige a la página que desees
            return redirect('shop')  # O usa otro nombre de URL adecuado, como 'success', si es necesario.
    else:
        formm = ContactoForm()

    # Renderiza la página con el formulario
    return render(request, 'contacto.html', {'formm': formm})



