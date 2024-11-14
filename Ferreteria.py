class Producto:
    def __init__(self, codigo, nombre, precio, cantidad):
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad

class Ferreteria:
    def __init__(self):
        self.inventario = {}

    def agregar_producto(self, producto):
        if producto.codigo not in self.inventario:
            self.inventario[producto.codigo] = producto
        else:
            self.inventario[producto.codigo].cantidad += producto.cantidad

    def realizar_venta(self, codigo, cantidad):
        if codigo in self.inventario and self.inventario[codigo].cantidad >= cantidad:
            producto = self.inventario[codigo]
            producto.cantidad -= cantidad
            return producto
        else:
            return None

    def generar_ticket(self, producto, cantidad):
        total = producto.precio * cantidad
        ticket = f"\n-------- TICKET --------\nProducto: {producto.nombre}\nCantidad: {cantidad}\nPrecio unitario: ${producto.precio}\nTotal: ${total}\n-------------------------"
        return ticket

def main():
    ferreteria = Ferreteria()

    producto1 = Producto("P1", "Martillo", 10.99, 50)
    producto2 = Producto("P2", "Destornillador", 5.99, 30)

    ferreteria.agregar_producto(producto1)
    ferreteria.agregar_producto(producto2)

    codigo_venta = input("Ingrese el código del producto a vender: ")
    cantidad_venta = int(input("Ingrese la cantidad a vender: "))

    producto_vendido = ferreteria.realizar_venta(codigo_venta, cantidad_venta)

    if producto_vendido:
        print(ferreteria.generar_ticket(producto_vendido, cantidad_venta))
    else:
        print("No hay suficiente stock para realizar la venta.")

if __name__ == "__Ferreteria__":
    Ferreteria()
    
