from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for 
from flask_mysqldb import MySQL
from conexion import config
from flask_login import LoginManager,login_user,logout_user,login_required
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash

#MODELS:
from models.ModelUser import ModelUser

#ENTITIES:
from models.entities.User import User



app = Flask(__name__)
csrf=CSRFProtect(app)
app.config['TESTING'] = False
db = MySQL(app)
login_manager_app = LoginManager(app)


@login_manager_app.user_loader
def loaduser(id):
    return ModelUser.get_by_id(db,id)

def status_401(error):
    return redirect(url_for('login'))

def status_404(error):
    return "<h1>Pagina no encontrada.</h1>"


@app.route('/')
@login_required
def index():
    return  redirect(url_for("home"))


def conector(a=1):
    cur = db.connection.cursor()
    if(a == 1):
        cur.execute("SELECT * FROM registros ORDER BY id DESC")
    if(a == 2):
        cur.execute("SELECT * FROM tarifas WHERE id = '8'")
    return cur.fetchall()



@app.route('/home')
@login_required
def home():
    

    
    return render_template('index.html', data = conector(1), tarifa = conector(2))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register' , methods=['GET','POST'])
@login_required
def register():
    if request.method == "POST":
        cur = db.connection.cursor()
        usuario = request.form['usuario']
        nombrecomp = request.form['nombrecomp']
        contrasenia = request.form['contrasenia']
        cur.execute('INSERT INTO usuarios_web (usuario, nombrecomp, contrasenia) VALUES (%s,%s,%s)' , (usuario,nombrecomp,generate_password_hash(contrasenia)))
        db.connection.commit()
    return render_template("register.html")


@app.route('/registros')
@login_required
def registros():
    cur = db.connection.cursor()
    cur.execute("SELECT * FROM registros ORDER BY id DESC")
    data = cur.fetchall()
    return render_template("registros.html" ,  data = data)

@app.route('/register_siga' , methods = ['GET', 'POST'])
@login_required
def register_siga():
    if request.method == "POST":
        cur = db.connection.cursor()
        usuario = request.form['usuario']
        contrasenia = request.form['contrasenia']
        privilegio = request.form['rol']
        rol = 3
        if(privilegio == "Administrador"):
            rol = 1
        elif(privilegio == "Cajero"):
            rol = 2


        cur.execute('INSERT INTO usuarios (usuario, password, privilegios) VALUES (%s,%s,%s)' , (usuario,contrasenia, rol))
        db.connection.commit()


    return render_template("register_siga.html")


@app.route('/tarifas')
@login_required
def tarifas():
    return render_template("tarifas.html")

@app.route('/protected')
@login_required
def protected():
    return "<h1>Esta vista es solo para usuarios.</h1>"

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == "POST":
        username = request.form['username']

        password = request.form['password']
        
        user = User(0, username,0,password)
        logged_user = ModelUser.login(db,user)
        
        if logged_user !=None:
            
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('home'))

            else:
                flash("Contraseña incorrecta.")
                return render_template('login.html')
        else:
            flash("Usuario no encontrado.")

    return render_template('login.html')











if __name__ == "__main__":
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401,status_401)
    app.register_error_handler(404,status_404)
    app.run()