
from django.urls import path
from .views import index, nosotros,formulario, api, producto, crear,modificar,eliminar,registrar,agregar_producto,restar_producto,eliminar_producto,limpiar_carrito,generarBoleta


urlpatterns =[
    path('', index, name='index'),
    path('nosotros/', nosotros, name='nosotros'), 
    path('formulario', formulario, name='formulario'),
    path('api', api, name='api'),
    path('producto/', producto, name="producto"),
    path('crear/', crear, name="crear"),
    path('modificar/<id>', modificar, name="modificar"),
    path('eliminar/<id>', eliminar, name="eliminar"),
    path('registrar/', registrar, name="registrar"),

    path('agregar/<id>', agregar_producto, name="agregar"),
    path('restar/<id>', restar_producto, name="restar"),
    path('eliminar2/<id>', eliminar_producto, name="eliminar2"),
    path('limpiar/', limpiar_carrito, name="limpiar"),
    path('generarBoleta/', generarBoleta,name="generarBoleta"),
   
    
    
    

]