from flask import Flask, render_template, send_from_directory, request, redirect, url_for, flash
from datetime import date
from flask_sqlalchemy import SQLAlchemy
import psycopg2

#PAGINA DE ALTA DE CONDUCTORES, VEHICULOS, ALMACENES Y RUTAS
app = Flask(__name__, template_folder="templates")
app.secret_key = 'mysecretkey'

#RUTAS
@app.route('/')
def home():
    return render_template("home.html", active_page="home")

# Configuración de la base de datos PostgreSQL en SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost/Amazon_Pola_Siero'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la base de datos
db = SQLAlchemy(app)
#------------------------CONDUCTORES-----------------------------
class Conductor(db.Model):
    __tablename__ = 'conductores'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    nif = db.Column(db.String(8), nullable=False)
    carnet = db.Column(db.String(2), nullable=False)
    tipo = db.Column(db.String(4), nullable=False)
    validez = db.Column(db.Date, nullable=False)
    nacimiento = db.Column(db.Date, nullable=False)
    centro_id = db.Column(db.Integer, nullable=False)

# Página principal para listar los conductores
@app.route('/conductores')
def conductores():
    conductores = Conductor.query.all()  # Obtenemos todos los conductores de la tabla 'conductores'
    return render_template("conductores.html", conductores=conductores, active_page="conductores")

# Ruta para agregar un nuevo conductor
@app.route('/add_conductor', methods=['GET', 'POST'])
def add_conductor():
    if request.method == 'POST':
        nombre = request.form['nombre']
        nif = request.form['nif']
        carnet = request.form['carnet']
        tipo = request.form['tipo']
        validez = request.form['validez']
        nacimiento = request.form['nacimiento']
        centro_id = request.form['centro_id']
        
        # Crear un nuevo objeto Conductor
        nuevo_conductor = Conductor(
            nombre=nombre,
            nif=nif,
            carnet=carnet,
            tipo=tipo,
            validez=date.fromisoformat(validez),
            nacimiento=date.fromisoformat(nacimiento),
            centro_id=centro_id
        )
        
        db.session.add(nuevo_conductor)
        db.session.commit()
        
        # Mensaje de éxito para verificar
        flash('Conductor añadido satisfactoriamente')
        return redirect(url_for('conductores'))
    
    return render_template('add_conductor.html')

@app.route('/edit_conductor/<int:id>', methods=['GET', 'POST'])
def edit_conductor(id):
    conductor = Conductor.query.get_or_404(id)
    if request.method == 'POST':
        conductor.nombre = request.form['nombre']
        conductor.nif = request.form['nif']
        conductor.carnet = request.form['carnet']
        conductor.tipo = request.form['tipo']
        conductor.validez = date.fromisoformat(request.form['validez'])
        conductor.nacimiento = date.fromisoformat(request.form['nacimiento'])
        conductor.centro_id = request.form['centro_id']
        
        db.session.commit()
        flash('Conductor actualizado correctamente')
        return redirect(url_for('conductores'))

    return render_template('edit_conductor.html', conductor=conductor)

@app.route('/delete_conductor/<int:id>', methods=['POST'])
def delete_conductor(id):
    conductor = Conductor.query.get_or_404(id) 
    db.session.delete(conductor) 
    db.session.commit()  
    flash('Conductor eliminado satisfactoriamente')  
    return redirect(url_for('conductores'))

@app.route('/imagenes/<path:filename>')
def custom_static(filename):
    return send_from_directory('imagenes', filename)
#------------------------VEHICULOS-----------------------------

class Vehiculo(db.Model):
    __tablename__ = 'vehiculos'
    id = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String(20), nullable=False)
    modelo = db.Column(db.String(50), nullable=False)
    placa = db.Column(db.String(8), nullable=False)
    precio = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    centro_id = db.Column(db.Integer, nullable=False)

@app.route('/vehiculos')
def vehiculos():
    vehiculos = Vehiculo.query.all()  # Obtenemos todos los conductores de la tabla 'conductores'
    return render_template("vehiculos.html", vehiculos=vehiculos, active_page="vehiculos")

@app.route('/add_vehiculo', methods=['GET', 'POST'])
def add_vehiculo():
    if request.method == 'POST':
        marca = request.form['marca']
        modelo = request.form['modelo']
        placa = request.form['placa']
        precio = request.form['precio']
        fecha = request.form['fecha']
        centro_id = request.form['centro_id']
        
        # Crear un nuevo objeto Conductor
        nuevo_vehiculo = Vehiculo(
            marca = marca,
            modelo = modelo,
            placa = placa,
            precio = precio,
            fecha = date.fromisoformat(fecha),
            centro_id=centro_id
        )
        
        db.session.add(nuevo_vehiculo)
        db.session.commit()
        
        # Mensaje de éxito para verificar
        flash('Vehículo añadido satisfactoriamente')
        return redirect(url_for('vehiculos'))
    
    return render_template('add_vehiculo.html')

@app.route('/edit_vehiculo/<int:id>', methods=['GET', 'POST'])
def edit_vehiculo(id):
    vehiculo = Vehiculo.query.get_or_404(id)
    if request.method == 'POST':
        vehiculo.marca = request.form['marca']
        vehiculo.modelo = request.form['modelo']
        vehiculo.placa = request.form['placa']
        vehiculo.precio = request.form['precio']
        vehiculo.fecha = date.fromisoformat(request.form['fecha'])
        vehiculo.centro_id = request.form['centro_id']
        
        db.session.commit()
        flash('Vehiculo actualizado correctamente')
        return redirect(url_for('vehiculos'))

    return render_template('edit_conductor.vehiculo.html', vehiculo=vehiculo)

@app.route('/delete_vehiculo/<int:id>', methods=['POST'])
def delete_vehiculo(id):
    vehiculo = Vehiculo.query.get_or_404(id) 
    db.session.delete(vehiculo) 
    db.session.commit()  
    flash('Vehiculo eliminado satisfactoriamente')  
    return redirect(url_for('vehiculos'))
#------------------------ALMACENES-----------------------------
class Almacen(db.Model):
    __tablename__ = 'centro'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(200), nullable=False)
    telefono = db.Column(db.Integer, nullable=False)
  
@app.route('/almacenes')
def almacenes():
    almacenes = Almacen.query.all()  # Obtenemos todos los conductores de la tabla 'conductores'
    return render_template("almacenes.html", almacenes=almacenes, active_page="almacenes")

@app.route('/add_almacen', methods=['GET', 'POST'])
def add_almacen():
    if request.method == 'POST':
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
             
        nuevo_almacen = Almacen(
            nombre = nombre,
            direccion = direccion,
            telefono = telefono,
        )
        
        db.session.add(nuevo_almacen)
        db.session.commit()
        
        # Mensaje de éxito para verificar
        flash('Almacén añadido satisfactoriamente')
        return redirect(url_for('almacenes'))
    
    return render_template('add_almacen.html')

@app.route('/edit_almacen/<int:id>', methods=['GET', 'POST'])
def edit_almacen(id):
    almacen = Almacen.query.get_or_404(id)
    if request.method == 'POST':
        almacen.nombre = request.form['nombre']
        almacen.direccion = request.form['direccion']
        almacen.telefono = request.form['telefono']
        
        db.session.commit()
        flash('Almacén actualizado correctamente')
        return redirect(url_for('almacenes'))

    return render_template('edit_almacen.html', almacen=almacen)

@app.route('/delete_almacen/<int:id>', methods=['POST'])
def delete_almacen(id):
    almacen = Almacen.query.get_or_404(id) 
    db.session.delete(almacen) 
    db.session.commit()  
    flash('Almacen eliminado satisfactoriamente')  
    return redirect(url_for('almacenes'))

#------------------------RUTAS-----------------------------

class Ruta(db.Model):
    __tablename__ = 'rutas'
    id = db.Column(db.Integer, primary_key=True)
    destino = db.Column(db.String(50), nullable=False)
    tiempo_estimado = db.Column(db.Integer, nullable=False)
    paquetes = db.Column(db.Integer, nullable=False)
    peso = db.Column(db.Float, nullable=False)
    centro_id = db.Column(db.Integer, nullable=False)
  
@app.route('/rutas')
def rutas():
    rutas = Ruta.query.all()  # Obtenemos todos los conductores de la tabla 'conductores'
    return render_template("rutas.html", rutas=rutas, active_page="rutas")

@app.route('/add_ruta', methods=['GET', 'POST'])
def add_ruta():
    if request.method == 'POST':
        destino = request.form['destino']
        tiempo_estimado = request.form['tiempo_estimado']
        paquetes = request.form['paquetes']
        peso = request.form['peso']
        centro_id = request.form['centro_id']
             
        nueva_ruta = Ruta(
            destino = destino,
            tiempo_estimado = tiempo_estimado,
            paquetes = paquetes,
            peso = peso,
            centro_id = centro_id
        )
        
        db.session.add(nueva_ruta)
        db.session.commit()
        
        # Mensaje de éxito para verificar
        flash('Ruta añadida satisfactoriamente')
        return redirect(url_for('rutas'))
    
    return render_template('add_ruta.html')

@app.route('/edit_ruta/<int:id>', methods=['GET', 'POST'])
def edit_ruta(id):
    ruta = Ruta.query.get_or_404(id)
    if request.method == 'POST':
        ruta.destino = request.form['destino']
        ruta.tiempo_estimado = request.form['tiempo_estimado']
        ruta.paquetes = request.form['paquetes']
        ruta.peso = request.form['peso']
        ruta.centro_id = request.form['centro_id']
        
        db.session.commit()
        flash('Ruta actualizada correctamente')
        return redirect(url_for('rutas'))

    return render_template('edit_ruta.html', ruta=ruta)

@app.route('/delete_ruta/<int:id>', methods=['POST'])
def delete_ruta(id):
    ruta = Ruta.query.get_or_404(id) 
    db.session.delete(ruta) 
    db.session.commit()  
    flash('Ruta eliminada satisfactoriamente')  
    return redirect(url_for('rutas'))

#------------------------CONTACTO Y LA EMPRESA-----------------------------

@app.route('/contacto') 
def contacto():
    return render_template("contacto.html", active_page="contacto")

@app.route('/la_empresa') 
def la_empresa():
    return render_template("la_empresa.html", active_page="la_empresa")


#run app
if __name__=='__main__':
    app.run(debug=True)

