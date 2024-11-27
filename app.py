from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Configuración de la base de datos
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  # Cambia esto si tienes contraseña
app.config['MYSQL_DB'] = 'ferreteria'

mysql = MySQL(app)

# Modelo base
class Producto:
    def __init__(self, id_producto, nombre, precio, imagen):
        self.id_producto = id_producto
        self.nombre = nombre
        self.precio = precio
        self.imagen = imagen

# Controlador
class Carrito:
    def __init__(self):
        if 'carrito' not in session:
            session['carrito'] = []

    def agregar_producto(self, producto):
        session['carrito'].append(producto.__dict__)
        session.modified = True

    def eliminar_producto(self, id_producto):
        session['carrito'] = [p for p in session['carrito'] if p['id_producto'] != id_producto]
        session.modified = True

    def obtener_carrito(self):
        return session.get('carrito', [])

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_user():
    correo = request.form['correo']
    contrasena = request.form['contrasena']

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE correo=%s AND contrasena=%s", (correo, contrasena))
    user = cursor.fetchone()

    if user:
        session['usuario'] = user[1]  # Nombre del usuario
        return redirect(url_for('productos'))
    else:
        return "Usuario o contraseña incorrectos"

@app.route('/registro')
def registro():
    return render_template('registro.html')

@app.route('/registro', methods=['POST'])
def registrar_usuario():
    usuario = request.form['usuario']
    correo = request.form['correo']
    contrasena = request.form['contrasena']

    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO usuarios (usuario, correo, contrasena) VALUES (%s, %s, %s)", (usuario, correo, contrasena))
    mysql.connection.commit()

    return redirect(url_for('login'))

@app.route('/productos')
def productos():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id_producto, nombre, precio, imagen FROM productos")
    productos = cursor.fetchall()
    return render_template('productos.html', productos=productos)

@app.route('/agregar_carrito/<int:id_producto>')
def agregar_carrito(id_producto):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id_producto, nombre, precio, imagen FROM productos WHERE id_producto = %s", (id_producto,))
    producto = cursor.fetchone()

    if producto:
        p = Producto(*producto)
        carrito = Carrito()
        carrito.agregar_producto(p)
    return redirect(url_for('ver_carrito'))

@app.route('/carrito')
def ver_carrito():
    carrito = Carrito()
    productos_en_carrito = carrito.obtener_carrito()
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id_producto, nombre, precio, imagen, descripcion FROM productos")
    productos_disponibles = cursor.fetchall()
    total = sum([float(item['precio']) for item in productos_en_carrito])  # Convertimos precios a flotantes
    return render_template('carrito.html', carrito=productos_en_carrito, productos=productos_disponibles, total=total)

@app.route('/eliminar_carrito/<int:id_producto>')
def eliminar_carrito(id_producto):
    carrito = Carrito()
    carrito.eliminar_producto(id_producto)
    return redirect(url_for('ver_carrito'))

@app.route('/comprar', methods=['POST'])
def comprar():
    carrito = Carrito()
    productos = carrito.obtener_carrito()

    cursor = mysql.connection.cursor()
    for producto in productos:
        cursor.execute("INSERT INTO compras (id_producto, nombre, precio) VALUES (%s, %s, %s)",
                       (producto['id_producto'], producto['nombre'], float(producto['precio'])))
    mysql.connection.commit()

    session.pop('carrito', None)
    return "Compra realizada con éxito"

if __name__ == '__main__':
    app.run(debug=True)
