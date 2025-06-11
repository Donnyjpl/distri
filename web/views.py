from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Categoria, Tag, Ingrediente,Producto,ProductoImagen
from .forms import CategoriaForm, TagForm, IngredienteForm,ProductoForm, ProductoImagenForm
from django.contrib import messages
from django.core.paginator import Paginator

# crud de categorias
def categoria_create(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categoria_list')
    else:
        form = CategoriaForm()
    return render(request, 'categoria/categoria_form.html', {'form': form})

def categoria_list(request):
    categorias = Categoria.objects.all()
    return render(request, 'categoria/categoria_list.html', {'categorias': categorias})

def categoria_delete(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        return redirect('categoria_list')
    return render(request, 'categoria/categoria_confirm_delete.html', {'categoria': categoria})

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
def tag_create(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tag_list')
    else:
        form = TagForm()
    return render(request, 'tag/tag_form.html', {'form': form})

def tag_list(request):
    tags= Tag.objects.all()
    return render(request, 'tag/tag_list.html', {'tags': tags})

def tag_delete(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    if request.method == 'POST':
        tag.delete()
        return redirect('tag_list')
    return render(request, 'tag/tag_confirm_delete.html', {'tag': tag})

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
def ingrediente_create(request):
    if request.method == 'POST':
        form = IngredienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ingrediente_list')
    else:
        form = TagForm()
    return render(request, 'ingrediente/ingrediente_form.html', {'form': form})

def ingrediente_list(request):
    ingredientes= Ingrediente.objects.all()
    return render(request, 'ingrediente/ingrediente_list.html', {'ingredientes': ingredientes})

def ingrediente_delete(request, pk):
    ingrediente = get_object_or_404(Ingrediente, pk=pk)
    if request.method == 'POST':
        ingrediente.delete()
        return redirect('ingrediente_list')
    return render(request, 'ingrediente/ingrediente_confirm_delete.html', {'ingrediente': ingrediente})

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
    return render(request, 'productos/detalle_producto.html', {'producto': producto})


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

def about(request):
    return render(request, 'about.html')

def index(request):
    return render(request, 'index1.html')