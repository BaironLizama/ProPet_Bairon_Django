import datetime
from django.db import models
from distutils.command.upload import upload
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import get_user
from django.db.models import F
from django.http import HttpRequest


# Create your models here.

class Categoria(models.Model):
    idCategoria = models.IntegerField(primary_key=True, verbose_name="Id de categoria")
    nombreCategoria=models.CharField(max_length=50, blank=True, verbose_name="Nombre de Categoria")

    def __str__(self):
        return self.nombreCategoria


class Producto(models.Model):
    codigo=models.CharField(primary_key=True, max_length=8, verbose_name="Codigo")
    nombre= models.CharField(max_length=50, verbose_name="Nombre")
    marca= models.CharField(max_length=50, verbose_name="Marca")
    stock=models.IntegerField( verbose_name="Stock")
    precio=models.IntegerField( verbose_name="Precio")
    categoria=models.ForeignKey(Categoria, on_delete=models.CASCADE, verbose_name="Categoria")
    imagen=models.ImageField(upload_to="imagenes", null=True, blank=True, verbose_name="Imagen")

    def __str__(self):
        return self.codigo
    

class Boleta(models.Model):
    
    id_boleta=models.AutoField(primary_key=True)
    total=models.BigIntegerField()
    fechaCompra=models.DateTimeField(blank=False, null=False, default = datetime.datetime.now)
    
    
    def __str__(self):
        return str(self.id_boleta)
    
    def descontar_stock(self):
        detalles = detalle_boleta.objects.filter(id_boleta=self.id_boleta)
        for detalle in detalles:
            producto = detalle.id_producto
            cantidad_vendida = detalle.cantidad
            producto.stock = F('stock') - cantidad_vendida
            producto.save()

class detalle_boleta(models.Model):
       
    id_boleta = models.ForeignKey('Boleta', blank=True, on_delete=models.CASCADE)
    id_detalle_boleta = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    nombre= models.CharField(max_length=50, verbose_name="Nombre")
    cantidad = models.IntegerField()
    subtotal = models.BigIntegerField()
    estado = models.CharField(max_length=40, default='procesando su pedido')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)

    def __str__(self):
        return str(self.id_detalle_boleta)
    
    