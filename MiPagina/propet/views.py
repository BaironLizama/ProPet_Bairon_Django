import datetime
from django.shortcuts import render, redirect
from .models import Producto, Boleta, detalle_boleta
from .forms import ProductoForm,RegistroUserForm
from django.contrib.auth.decorators import login_required, user_passes_test 
from django.contrib.auth import authenticate, login
from propet.compra import Carrito






#from .forms import CategoriaForm

# Create your views here.

def index(request):
    return render(request,'index.html')

def nosotros(request):
    return render(request,'nosotros.html')



def formulario(request):
    return render(request,'formulario.html')

def api(request):
    return render(request,'api.html')

def crear(request):
    return render(request,'crear.html')

def admin_check(user):
    return user.is_superuser  # Verifica si el usuario es un administrador


#def producto(request):
#    return render(request,'producto.html')


def producto(request):
    productitos = Producto.objects.raw('Select * from propet_producto')
    datos={
        'propet':productitos
    }
    return render(request, 'producto.html', datos)

@login_required
@user_passes_test(admin_check)
def crear(request):
    if request.method=="POST":
        productoform=ProductoForm(request.POST,request.FILES)
        if productoform.is_valid():
            productoform.save()     #similar al insert en función
            return redirect ('producto')
    else:
        productoform=ProductoForm()
    return render (request, 'crear.html', {'productoform': productoform})


@login_required
@user_passes_test(admin_check)
def eliminar(request, id): 
    vehiculoEliminado = Producto.objects.get(codigo=id) #similar a select * from... where...
    vehiculoEliminado.delete()
    return redirect ('producto')

@login_required
@user_passes_test(admin_check)
def modificar(request, id): 
    productoModificado=Producto.objects.get(codigo=id) #buscamos el objeto
    datos ={
        'form':ProductoForm(instance=productoModificado)
    }
    if request.method=="POST":
        formulario = ProductoForm(data=request.POST, instance=productoModificado, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect ('producto')
    return render(request, 'modificar.html', datos)



def registrar(request):
    data = {
        'form' : RegistroUserForm()
    }
    if request.method=="POST":
        formulario = RegistroUserForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"], 
                                password = formulario.cleaned_data["password1"])
            login(request, user)
            return redirect ('index')
        data["form"] = formulario
    return render(request, 'registration/registro.html', data)



def agregar_producto(request,id):
    carrito_compra= Carrito(request)
    producto = Producto.objects.get(codigo=id)
    carrito_compra.agregar(producto=producto)
    return redirect('producto')

def eliminar_producto(request, id):
    carrito_compra= Carrito(request)
    producto = Producto.objects.get(codigo=id)
    carrito_compra.eliminar(producto=producto)
    return redirect('producto')



def restar_producto(request, id):
    carrito_compra= Carrito(request)
    producto = Producto.objects.get(codigo=id)
    carrito_compra.restar(producto=producto)
    return redirect('producto')

def limpiar_carrito(request):
    carrito_compra= Carrito(request)
    carrito_compra.limpiar()
    return redirect('producto')  


def generarBoleta(request):
    # Verifica si el carrito está vacío
    if len(request.session['carrito']) == 0:
        
        return redirect('producto')  
   
    precio_total = 0
    for key, value in request.session['carrito'].items():
        precio_total += int(value['precio']) * int(value['cantidad'])
    
    costo_envio = 0
    if precio_total < 20000:
        costo_envio = 2000  
        precio_total += costo_envio
    
    boleta = Boleta(total=precio_total)
    boleta.save()
    
    productos = []
    for key, value in request.session['carrito'].items():
        producto = Producto.objects.get(codigo=value['producto_id'])
        cant = value['cantidad']
        subtotal = cant * int(value['precio'])
        detalle = detalle_boleta(id_boleta=boleta, id_producto=producto, cantidad=cant, subtotal=subtotal, usuario=request.user)
        detalle.save()
        productos.append({
            'id_boleta': detalle.id_boleta,
            'id_producto': detalle.id_producto,
            'nombre': producto.nombre,  
            'cantidad': detalle.cantidad,
            'subtotal': detalle.subtotal
        })
    
    boleta.descontar_stock()
    
    datos = {
        'productos': productos,
        'fecha': boleta.fechaCompra,
        'total': boleta.total,
        'costo_envio': costo_envio,  
        'usuario': request.user.username 
    }
    
    request.session['boleta'] = boleta.id_boleta
    carrito = Carrito(request)
    carrito.limpiar()
    
    return render(request, 'detallecarrito.html', datos)
    























