from flask import Flask, render_template, redirect, url_for, request, flash, send_file
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db
from models.usuario import Usuario
from models.cliente import Cliente
from models.ramo import Ramo
from models.pedido import Pedido
from datetime import datetime
import os
from fpdf import FPDF

app = Flask(__name__)
app.secret_key = 'juli_flowers_clave_secreta_2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/juli_flowers?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/img')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Debes iniciar sesión para acceder a esta sección"
login_manager.login_message_category = "warning"

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

@app.route('/')
def inicio():
    return render_template('inicio.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contactos')
def contactos():
    return render_template('contactos.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('inicio'))
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = Usuario.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('inicio'))
        flash('Correo o contraseña incorrectos', 'danger')
    
    return render_template('login.html')

@app.route('/registro', methods=['GET','POST'])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for('inicio'))
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']
        
        if Usuario.query.filter_by(email=email).first():
            flash('El correo ya está registrado', 'danger')
            return redirect(url_for('registro'))
        
        nuevo_usuario = Usuario(nombre=nombre, email=email)
        nuevo_usuario.set_password(password)
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        flash('Registro exitoso! Inicia sesión', 'success')
        return redirect(url_for('login'))
    
    return render_template('registro.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada correctamente', 'success')
    return redirect(url_for('inicio'))

@app.route('/productos')
@login_required
def productos():
    buscar = request.args.get('buscar', '')
    if buscar:
        productos = Ramo.query.filter(Ramo.nombre_ramo.like(f'%{buscar}%')).all()
    else:
        productos = Ramo.query.all()
    return render_template('productos.html', productos=productos, buscar=buscar)

@app.route('/productos/nuevo', methods=['GET','POST'])
@login_required
def nuevo_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = float(request.form['precio'])
        
        archivo = request.files['imagen']
        imagen = 'ramo_default.jpg'
        if archivo and archivo.filename != '':
            imagen = archivo.filename
            archivo.save(os.path.join(app.config['UPLOAD_FOLDER'], imagen))
        
        nuevo_producto = Ramo(
            nombre_ramo=nombre,
            descripcion_ramo=descripcion,
            precio_total=precio,
            imagen_ramo=imagen
        )
        db.session.add(nuevo_producto)
        db.session.commit()
        
        flash('Producto agregado correctamente', 'success')
        return redirect(url_for('productos'))
    
    return render_template('nuevo_producto.html')

@app.route('/productos/editar/<int:id>', methods=['GET','POST'])
@login_required
def editar_producto(id):
    producto = Ramo.query.get_or_404(id)
    
    if request.method == 'POST':
        producto.nombre_ramo = request.form['nombre']
        producto.descripcion_ramo = request.form['descripcion']
        producto.precio_total = float(request.form['precio'])
        
        archivo = request.files['imagen']
        if archivo and archivo.filename != '':
            producto.imagen_ramo = archivo.filename
            archivo.save(os.path.join(app.config['UPLOAD_FOLDER'], archivo.filename))
        
        db.session.commit()
        flash('Producto actualizado correctamente', 'success')
        return redirect(url_for('productos'))
    
    return render_template('nuevo_producto.html', producto=producto)

@app.route('/productos/eliminar/<int:id>')
@login_required
def eliminar_producto(id):
    producto = Ramo.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    
    flash('Producto eliminado correctamente', 'info')
    return redirect(url_for('productos'))

@app.route('/clientes')
@login_required
def clientes():
    buscar = request.args.get('buscar', '')
    if buscar:
        clientes = Cliente.query.filter(
            (Cliente.nombre_cliente.like(f'%{buscar}%')) | 
            (Cliente.apellido_cliente.like(f'%{buscar}%')) |
            (Cliente.ci_cliente.like(f'%{buscar}%'))
        ).all()
    else:
        clientes = Cliente.query.all()
    return render_template('clientes.html', clientes=clientes, buscar=buscar)

@app.route('/clientes/nuevo', methods=['GET','POST'])
@login_required
def nuevo_cliente():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        telefono = request.form['telefono']
        ci = request.form['ci']
        direccion = request.form['direccion']
        
        if Cliente.query.filter_by(email_cliente=email).first():
            flash('El correo ya está registrado', 'danger')
            return redirect(url_for('nuevo_cliente'))
        
        if Cliente.query.filter_by(ci_cliente=ci).first():
            flash('La CI ya está registrada', 'danger')
            return redirect(url_for('nuevo_cliente'))
        
        nuevo_cliente = Cliente(
            nombre_cliente=nombre,
            apellido_cliente=apellido,
            email_cliente=email,
            telefono_cliente=telefono,
            ci_cliente=ci,
            direccion_cliente=direccion
        )
        db.session.add(nuevo_cliente)
        db.session.commit()
        
        flash('Cliente registrado correctamente', 'success')
        return redirect(url_for('clientes'))
    
    return render_template('nuevo_cliente.html')

@app.route('/clientes/editar/<int:id>', methods=['GET','POST'])
@login_required
def editar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    
    if request.method == 'POST':
        cliente.nombre_cliente = request.form['nombre']
        cliente.apellido_cliente = request.form['apellido']
        cliente.email_cliente = request.form['email']
        cliente.telefono_cliente = request.form['telefono']
        cliente.ci_cliente = request.form['ci']
        cliente.direccion_cliente = request.form['direccion']
        
        db.session.commit()
        flash('Cliente actualizado correctamente', 'success')
        return redirect(url_for('clientes'))
    
    return render_template('nuevo_cliente.html', cliente=cliente)

@app.route('/clientes/eliminar/<int:id>')
@login_required
def eliminar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    db.session.delete(cliente)
    db.session.commit()
    
    flash('Cliente eliminado correctamente', 'info')
    return redirect(url_for('clientes'))

@app.route('/pedidos')
@login_required
def pedidos():
    buscar = request.args.get('buscar', '')
    if buscar:
        pedidos = Pedido.query.join(Cliente).filter(
            (Cliente.nombre_cliente.like(f'%{buscar}%')) | 
            (Cliente.apellido_cliente.like(f'%{buscar}%'))
        ).all()
    else:
        pedidos = Pedido.query.all()
    return render_template('pedidos.html', pedidos=pedidos, buscar=buscar)

@app.route('/pedidos/nuevo', methods=['GET','POST'])
@login_required
def nuevo_pedido():
    clientes = Cliente.query.all()
    productos = Ramo.query.all()
    
    if request.method == 'POST':
        id_cliente = int(request.form['cliente'])
        id_ramo = int(request.form['producto'])
        cantidad = int(request.form['cantidad'])
        fecha = datetime.strptime(request.form['fecha'], '%Y-%m-%d')
        estado = request.form['estado']
        total = float(request.form['total'])
        
        nuevo_pedido = Pedido(
            id_cliente=id_cliente,
            id_ramo=id_ramo,
            cantidad=cantidad,
            fecha_entrega=fecha,
            estado_pedido=estado,
            total_pedido=total
        )
        db.session.add(nuevo_pedido)
        db.session.commit()
        
        flash('Pedido registrado correctamente', 'success')
        return redirect(url_for('pedidos'))
    
    return render_template('nuevo_pedido.html', clientes=clientes, productos=productos)

@app.route('/pedidos/eliminar/<int:id>')
@login_required
def eliminar_pedido(id):
    pedido = Pedido.query.get_or_404(id)
    db.session.delete(pedido)
    db.session.commit()
    
    flash('Pedido eliminado correctamente', 'info')
    return redirect(url_for('pedidos'))

@app.route('/reporte')
@login_required
def reporte():
    return render_template('reporte.html')

@app.route('/reporte-pedidos')
@login_required
def reporte_pedidos():
    pedidos = Pedido.query.join(Cliente).join(Ramo).all()
    total_general = sum(pedido.total_pedido for pedido in pedidos)
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, txt="REPORTE DE PEDIDOS - JULI FLOWERS", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt=f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(20, 10, "ID", 1)
    pdf.cell(40, 10, "CLIENTE", 1)
    pdf.cell(40, 10, "PRODUCTO", 1)
    pdf.cell(20, 10, "CANT.", 1)
    pdf.cell(30, 10, "FECHA ENTREGA", 1)
    pdf.cell(25, 10, "ESTADO", 1)
    pdf.cell(25, 10, "TOTAL", 1, ln=True)
    
    pdf.set_font("Arial", size=12)
    for pedido in pedidos:
        pdf.cell(20, 10, str(pedido.id_pedido), 1)
        pdf.cell(40, 10, f"{pedido.cliente.nombre_cliente} {pedido.cliente.apellido_cliente}", 1)
        pdf.cell(40, 10, pedido.ramo.nombre_ramo, 1)
        pdf.cell(20, 10, str(pedido.cantidad), 1)
        pdf.cell(30, 10, pedido.fecha_entrega.strftime('%d/%m/%Y'), 1)
        pdf.cell(25, 10, pedido.estado_pedido, 1)
        pdf.cell(25, 10, f"${pedido.total_pedido:.2f}", 1, ln=True)
    
    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(175, 10, txt=f"TOTAL GENERAL DE PEDIDOS: ${total_general:.2f}", ln=True, align='R')
    
    pdf.output("reporte_juli_flowers.pdf")
    return send_file("reporte_juli_flowers.pdf", as_attachment=True)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)