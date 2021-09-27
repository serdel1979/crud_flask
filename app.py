from flask import Flask, render_template, request, redirect, url_for, flash
from flask.wrappers import Request
from flask_mysqldb import MySQL

app = Flask(__name__)


#conexion sql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'flaskcontacts'
mysql = MySQL(app)

#conf de sesion 
app.secret_key = 'mysecretkey'



@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    datos = cur.fetchall() 
    return render_template('index.html', contactos = datos)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
       fullname = request.form['fullname'] 
       phone = request.form['phone']
       email = request.form['email']
       """Controlo que las variables recibidas del formulario no estén vacías"""
       if fullname and phone and email:
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO contacts (fullname, phone, email) VALUES (%s, %s, %s)',(fullname, phone, email))
            mysql.connection.commit()
            flash('Contacto agregado!!!')
       else:
            flash('No se guardó nada!!!')
       return redirect(url_for('Index'))

@app.route('/edit/<id>')
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = %s',(id))
    dato = cur.fetchall()
    return render_template('edit_contacto.html',contacto = dato[0])



@app.route('/update/<id>', methods = ['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname'] 
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE contacts
            SET fullname = %s,
                phone = %s,
                email = %s
            WHERE id = %s
            """,(fullname,phone,email,id))
        mysql.connection.commit()
        flash('Contacto actualizado!!!')
        return redirect(url_for('Index'))




@app.route('/delete/<string:id>')
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Eliminado!!!')
    return redirect(url_for('Index'))




if __name__ == '__main__':
    app.run(port = 3000, debug = True)