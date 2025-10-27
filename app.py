from flask import Flask, render_template, request, redirect, url_for, flash
from crud_productos import ProductoCRUD

app = Flask(__name__)
app.secret_key = 'clave-secreta-123'  # Necesario para flash messages
crud = ProductoCRUD()

@app.route('/')
def index():
    productos = []
    keys = crud.r.scan_iter(match='producto:*')
    for k in keys:
        prod = crud.r.hgetall(k)
        prod['id'] = k.split(':')[1]
        productos.append(prod)
    return render_template('index.html', productos=productos)

@app.route('/producto/nuevo', methods=['GET', 'POST'])
def nuevo_producto():
    if request.method == 'POST':
        id = request.form['id']
        nombre = request.form['nombre']
        precio = request.form['precio']
        stock = request.form['stock']
        
        crud.crear(id, nombre, precio, stock)
        flash('Producto creado exitosamente')
        return redirect(url_for('index'))
    return render_template('nuevo.html')

@app.route('/producto/editar/<id>', methods=['GET', 'POST'])
def editar_producto(id):
    if request.method == 'POST':
        datos = {
            'nombre': request.form['nombre'],
            'precio': request.form['precio'],
            'stock': request.form['stock']
        }
        crud.actualizar(id, datos)
        flash('Producto actualizado exitosamente')
        return redirect(url_for('index'))
    
    producto = crud.leer(id)
    if not producto:
        flash('Producto no encontrado')
        return redirect(url_for('index'))
    producto['id'] = id
    return render_template('editar.html', producto=producto)

@app.route('/producto/eliminar/<id>')
def eliminar_producto(id):
    crud.eliminar(id)
    flash('Producto eliminado exitosamente')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)