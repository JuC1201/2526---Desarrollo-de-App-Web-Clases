from flask import Flask, render_template, url_for, request, redirect, flash
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/usuario/<nombre>')
def usuario(nombre):
    return f'Bienvenido, {nombre}!'

@app.route('/contactos')
def contact():
    return 'Página de contactos'  # Texto plano en lugar de render_template

@app.route('/about')
def about():
    return 'Página acerca de nosotros'  # Texto plano en lugar de render_template

if __name__ == '__main__':
    app.run(debug=True)