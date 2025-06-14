# compras/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from web.models import Producto
from .models import Carrito, ItemCarrito
from django.contrib import messages
from django.shortcuts import redirect


@login_required
def ver_carrito(request):
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    
    
    envio = request.session.get('envio', 'retiro')

    if envio == 'centro':
        costo_envio = 10
    elif envio == 'provincia':
        costo_envio = 15
    else:  # retiro en tienda
        costo_envio = 0

    total = carrito.total + costo_envio

    context = {
        'carrito': carrito,
        'envio': envio,
        'costo_envio': costo_envio,
        'total': total,
    }
    return render(request, 'carrito/carrito.html', context)


@login_required
def agregar_al_carrito(request, slug):
    producto = get_object_or_404(Producto, slug=slug)
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    cantidad = int(request.POST.get('cantidad', 1))  # Captura cantidad, default 1
    
    # Aquí procesa talla y color si aplican, según tu modelo

    item, creado = ItemCarrito.objects.get_or_create(carrito=carrito, producto=producto)
    if not creado:
        item.cantidad += cantidad
    else:
        item.cantidad = cantidad
    item.save()

    messages.success(request, f'{producto.nombre} agregado al carrito.')
    return redirect('ver_carrito')


# compras/views.py
@login_required
def eliminar_del_carrito(request, slug):
    producto = get_object_or_404(Producto, slug=slug)
    carrito = get_object_or_404(Carrito, usuario=request.user)
    item = carrito.items.filter(producto=producto).first()

    if item:
        item.delete()
        messages.info(request, f"{producto.nombre} eliminado del carrito.")
    else:
        messages.warning(request, f"El producto no se encontró en tu carrito.")

    return redirect('ver_carrito')

@login_required
def actualizar_cantidad_carrito(request, slug):
    producto = get_object_or_404(Producto, slug=slug)
    carrito = get_object_or_404(Carrito, usuario=request.user)
    item = carrito.items.filter(producto=producto).first()

    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad', 1))
        if item:
            if cantidad > 0:
                item.cantidad = cantidad
                item.save()
                messages.success(request, 'Cantidad actualizada.')
            else:
                item.delete()
                messages.info(request, 'Producto eliminado del carrito por cantidad 0.')
    return redirect('ver_carrito')


@login_required
def actualizar_envio(request):
    if request.method == "POST":
        envio = request.POST.get('envio', 'retiro')
        request.session['envio'] = envio
    return redirect('ver_carrito')

