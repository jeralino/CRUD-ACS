from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import os

# Configuración de la aplicación
app = Flask(__name__)
app.secret_key = "my_secret_key"

# Configuración de la base de datos
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "your_user"
app.config["MYSQL_PASSWORD"] = "your_password"
app.config["MYSQL_DB"] = "your_database"

mysql = MySQL(app)

# Ruta principal: lista todos los elementos
@app.route('/')
def index():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM items")
        items = cursor.fetchall()
        return render_template('index.html', items=items)
    except Exception as e:
        flash(f"Error fetching items: {str(e)}")
        return render_template('index.html', items=[])

# Ruta para añadir un nuevo elemento
@app.route('/add', methods=['POST'])
def add_item():
    name = request.form.get('name')
    if not name:
        flash('Item name cannot be empty!')
        return redirect(url_for('index'))
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO items (name) VALUES (%s)", (name,))
        mysql.connection.commit()
        flash('Item added successfully!')
    except Exception as e:
        flash(f"Error adding item: {str(e)}")
    return redirect(url_for('index'))

# Ruta para editar un elemento existente
@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit_item(id):
    cursor = mysql.connection.cursor()
    try:
        if request.method == 'POST':
            name = request.form.get('name')
            if not name:
                flash('Item name cannot be empty!')
                return redirect(url_for('edit_item', id=id))
            cursor.execute("UPDATE items SET name = %s WHERE id = %s", (name, id))
            mysql.connection.commit()
            flash('Item updated successfully!')
            return redirect(url_for('index'))
        cursor.execute("SELECT * FROM items WHERE id = %s", (id,))
        item = cursor.fetchone()
        return render_template('edit.html', item=item)
    except Exception as e:
        flash(f"Error editing item: {str(e)}")
        return redirect(url_for('index'))

# Ruta para eliminar un elemento
@app.route('/delete/<id>')
def delete_item(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM items WHERE id = %s", (id,))
        mysql.connection.commit()
        flash('Item deleted successfully!')
    except Exception as e:
        flash(f"Error deleting item: {str(e)}")
    return redirect(url_for('index'))

# Iniciar el servidor
if __name__ == '__main__':
    app.run(debug=True)
