from .models import Producto, detalle_boleta


class Carrito:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        carrito = self.session.get("carrito")
        if not carrito:
            carrito = self.session["carrito"] = {}
        self.carrito=carrito 

    def agregar(self, producto):
        if producto.stock > 0:
            if producto.codigo not in self.carrito.keys():
                self.carrito[producto.codigo] = {
                    "producto_id": producto.codigo,
                    "nombre": producto.nombre, 
                    "marca": producto.marca,
                    "stock": producto.stock,
                    "precio": str(producto.precio),
                    "cantidad": 1,
                    "total": producto.precio,
                }
            else:
                for key, value in self.carrito.items():
                    if key == producto.codigo:
                        if value["cantidad"] < value["stock"]:
                            value["cantidad"] += 1
                            value["precio"] = producto.precio
                            value["total"] += producto.precio
                        # Si la cantidad ya iguala al stock, no se agrega más cantidad
                        break
            self.guardar_carrito()
    
    def guardar_carrito(self):
        self.session["carrito"] = self.carrito
        self.session.modified=True 
 

    def eliminar(self, producto):
        id = producto.codigo
        if id in self.carrito: 
            del self.carrito[id]
            self.guardar_carrito()    

    
    
    def restar(self, producto):
        for key, value in self.carrito.items():
            if key == producto.codigo:
                if value["cantidad"] > 1:
                    value["cantidad"] -= 1
                    value["total"] -= producto.precio
                # Si la cantidad es 1, se elimina el producto del carrito
                elif value["cantidad"] == 1:
                    self.eliminar(producto)
                break
        self.guardar_carrito()

    def limpiar(self):
        self.session["carrito"]={}
        self.session.modified=True

    
        