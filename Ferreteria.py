import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem, QInputDialog
from PyQt5.QtGui import QFont, QTextDocument
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtCore import QDateTime
import mysql.connector 

class FerreteriaApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ferretería - Sistema de Ventas")
        self.setGeometry(100, 100, 600, 400)

        # Conexión a la base de datos
        self.conexion = self.conectar_db()

        # Variables para agregar o editar producto
        self.id_producto = QLineEdit()
        self.nombre_producto = QLineEdit()
        self.precio_publico = QLineEdit()
        self.precio_distribuidor = QLineEdit()
        self.stock = QLineEdit()

        # Variables para realizar ventas
        self.id_producto_venta = QLineEdit()
        self.producto_venta = QLineEdit()
        self.cantidad = QLineEdit()
        self.carrito = []
        self.tipo_precio_venta = "publico"

        self.crear_interfaz()

    def conectar_db(self):
        try:
            conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="ferreteria"
            )
            QMessageBox.information(self, "Conexión", "Conexión a la base de datos exitosa.")
            return conexion
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Error", f"Error al conectar a la base de datos: {err}")
            sys.exit()

    def crear_interfaz(self):
        layout = QVBoxLayout()

        # Sección de agregar productos
        titulo_productos = QLabel("Agregar/Editar Producto")
        titulo_productos.setFont(QFont("Arial", 14))
        layout.addWidget(titulo_productos)

        form_layout = QHBoxLayout()
        form_layout.addWidget(QLabel("ID (Para Editar):"))
        form_layout.addWidget(self.id_producto)
        layout.addLayout(form_layout)

        form_layout = QHBoxLayout()
        form_layout.addWidget(QLabel("Nombre:"))
        form_layout.addWidget(self.nombre_producto)
        layout.addLayout(form_layout)

        form_layout = QHBoxLayout()
        form_layout.addWidget(QLabel("Precio Público:"))
        form_layout.addWidget(self.precio_publico)
        layout.addLayout(form_layout)

        form_layout = QHBoxLayout()
        form_layout.addWidget(QLabel("Precio Distribuidor:"))
        form_layout.addWidget(self.precio_distribuidor)
        layout.addLayout(form_layout)

        form_layout = QHBoxLayout()
        form_layout.addWidget(QLabel("Stock:"))
        form_layout.addWidget(self.stock)
        layout.addLayout(form_layout)

        btn_layout = QHBoxLayout()
        btn_agregar = QPushButton("Agregar Producto")
        btn_agregar.clicked.connect(self.agregar_producto)
        btn_editar = QPushButton("Editar Producto")
        btn_editar.clicked.connect(self.editar_producto)
        btn_layout.addWidget(btn_agregar)
        btn_layout.addWidget(btn_editar)
        layout.addLayout(btn_layout)

        layout.addWidget(QLabel("-" * 30))

        # Sección de ventas
        titulo_ventas = QLabel("Realizar Venta")
        titulo_ventas.setFont(QFont("Arial", 14))
        layout.addWidget(titulo_ventas)

        form_layout = QHBoxLayout()
        form_layout.addWidget(QLabel("ID del Producto (opcional):"))
        form_layout.addWidget(self.id_producto_venta)
        layout.addLayout(form_layout)

        form_layout = QHBoxLayout()
        form_layout.addWidget(QLabel("Nombre del Producto (opcional):"))
        form_layout.addWidget(self.producto_venta)
        layout.addLayout(form_layout)

        form_layout = QHBoxLayout()
        form_layout.addWidget(QLabel("Cantidad:"))
        form_layout.addWidget(self.cantidad)
        layout.addLayout(form_layout)

        btn_layout = QHBoxLayout()
        btn_agregar_carrito = QPushButton("Agregar al Carrito")
        btn_agregar_carrito.clicked.connect(self.agregar_carrito)
        btn_finalizar_venta = QPushButton("Finalizar Venta")
        btn_finalizar_venta.clicked.connect(self.elegir_tipo_precio)
        btn_layout.addWidget(btn_agregar_carrito)
        btn_layout.addWidget(btn_finalizar_venta)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def agregar_producto(self):
        nombre = self.nombre_producto.text()
        precio_publico = float(self.precio_publico.text() or 0)
        precio_distribuidor = float(self.precio_distribuidor.text() or 0)
        stock = int(self.stock.text() or 0)

        if nombre and precio_publico > 0 and precio_distribuidor > 0 and stock >= 0:
            cursor = self.conexion.cursor()
            cursor.execute(
                "INSERT INTO productos (nombre, precio_publico, precio_distribuidor, stock) VALUES (%s, %s, %s, %s)",
                (nombre, precio_publico, precio_distribuidor, stock)
            )
            self.conexion.commit()
            QMessageBox.information(self, "Éxito", f"Producto '{nombre}' agregado con éxito al inventario")
            self.limpiar_campos_producto()
        else:
            QMessageBox.warning(self, "Error", "Por favor, completa todos los campos correctamente.")

    def editar_producto(self):
        id_producto = int(self.id_producto.text() or 0)
        nombre = self.nombre_producto.text()
        precio_publico = float(self.precio_publico.text() or 0)
        precio_distribuidor = float(self.precio_distribuidor.text() or 0)
        stock = int(self.stock.text() or 0)

        if id_producto:
            cursor = self.conexion.cursor()
            consulta = "UPDATE productos SET "
            valores = []
            cambios = []

            if nombre:
                cambios.append("nombre = %s")
                valores.append(nombre)
            if precio_publico > 0:
                cambios.append("precio_publico = %s")
                valores.append(precio_publico)
            if precio_distribuidor > 0:
                cambios.append("precio_distribuidor = %s")
                valores.append(precio_distribuidor)
            if stock >= 0:
                cambios.append("stock = %s")
                valores.append(stock)
            
            if cambios:
                consulta += ", ".join(cambios) + " WHERE id = %s"
                valores.append(id_producto)

                cursor.execute(consulta, valores)
                self.conexion.commit()
                QMessageBox.information(self, "Éxito", f"Producto con ID {id_producto} actualizado correctamente.")
                self.limpiar_campos_producto()
            else:
                QMessageBox.warning(self, "Error", "No se han detectado cambios para actualizar.")
        else:
            QMessageBox.warning(self, "Error", "Por favor, introduce el ID del producto para actualizar.")

    def limpiar_campos_producto(self):
        self.id_producto.clear()
        self.nombre_producto.clear()
        self.precio_publico.clear()
        self.precio_distribuidor.clear()
        self.stock.clear()

    def agregar_carrito(self):
        id_producto = self.id_producto_venta.text()
        nombre_producto = self.producto_venta.text()
        cantidad = int(self.cantidad.text() or 0)

        if (id_producto or nombre_producto) and cantidad > 0:
            cursor = self.conexion.cursor()
            if id_producto:
                cursor.execute("SELECT * FROM productos WHERE id = %s", (id_producto,))
            else:
                cursor.execute("SELECT * FROM productos WHERE nombre = %s", (nombre_producto,))
            
            producto = cursor.fetchone()
            if producto:
                self.carrito.append({
                    'id': producto[0],
                    'nombre': producto[1],
                    'precio_publico': producto[2],
                    'precio_distribuidor': producto[3],
                    'cantidad': cantidad
                })
                QMessageBox.information(self, "Éxito", f"Producto agregado al carrito: {producto[1]} x {cantidad}")
                self.limpiar_campos_venta()
            else:
                QMessageBox.warning(self, "Error", "Producto no encontrado.")
        else:
            QMessageBox.warning(self, "Error", "Por favor, introduce el ID o nombre del producto y la cantidad.")

    def limpiar_campos_venta(self):
        self.id_producto_venta.clear()
        self.producto_venta.clear()
        self.cantidad.clear()

    def elegir_tipo_precio(self):
        if not self.carrito:
            QMessageBox.warning(self, "Error", "El carrito está vacío.")
            return

        tipo_precio, ok = QInputDialog.getItem(self, "Tipo de Precio", "Seleccione el tipo de precio:", ["Público", "Distribuidor"], 0, False)
        if ok:
            self.tipo_precio_venta = "publico" if tipo_precio == "Público" else "distribuidor"
            self.finalizar_venta()

    def finalizar_venta(self):
        if not self.carrito:
            QMessageBox.warning(self, "Error", "El carrito está vacío.")
            return

        total = sum(item['precio_publico' if self.tipo_precio_venta == 'publico' else 'precio_distribuidor'] * item['cantidad'] for item in self.carrito)
        
        detalle = "Ferretería - Ticket de Venta\n"
        detalle += f"Fecha: {QDateTime.currentDateTime().toString('dd/MM/yyyy HH:mm:ss')}\n\n"
        detalle += f"{'Producto':<30}{'Cant.':<10}{'Precio':<15}{'Subtotal':<15}\n"
        detalle += "-" * 70 + "\n"
        
        for item in self.carrito:
            precio = item['precio_publico' if self.tipo_precio_venta == 'publico' else 'precio_distribuidor']
            subtotal = precio * item['cantidad']
            detalle += f"{item['nombre']:<30}{item['cantidad']:<10}${precio:<15.2f}${subtotal:<15.2f}\n"
        
        detalle += "-" * 70 + "\n"
        detalle += f"{'Total:':<55}${total:.2f}\n"
        
        # Mostrar resumen de la venta
        QMessageBox.information(self, "Venta Finalizada", detalle)
        
        # Imprimir el ticket
        self.imprimir_ticket(detalle)
        
        # Actualizar el stock en la base de datos
        cursor = self.conexion.cursor()
        for item in self.carrito:
            cursor.execute("UPDATE productos SET stock = stock - %s WHERE id = %s", (item['cantidad'], item['id']))
        self.conexion.commit()
        
        self.carrito.clear()

    def imprimir_ticket(self, detalle):
        printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog(printer, self)
        
        if dialog.exec_() == QPrintDialog.Accepted:
            document = QTextDocument()
            document.setPlainText(detalle)
            document.print_(printer)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = FerreteriaApp()
    ventana.show()
    sys.exit(app.exec_())
