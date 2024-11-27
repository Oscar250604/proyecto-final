from flask import session

class Carrito:
    def __init__(self):
        if 'carrito' not in session:
            session['carrito'] = []

    def agregar_producto(self, producto):
        session['carrito'].append({
            'id_producto': producto.id_producto,
            'nombre': producto.nombre,
            'precio': float(producto.precio),  # Convertimos el precio a número
            'imagen': producto.imagen
        })
        session.modified = True

    def eliminar_producto(self, id_producto):
        session['carrito'] = [p for p in session['carrito'] if p['id_producto'] != id_producto]
        session.modified = True

    def obtener_carrito(self):
        return session.get('carrito', [])
