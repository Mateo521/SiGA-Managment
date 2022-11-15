from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for 
from flask_mysqldb import MySQL
from conexion import config
from flask_login import LoginManager,login_user,logout_user,login_required
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash
from datetime import datetime


#MODELS:
from models.ModelUser import ModelUser

#ENTITIES:
from models.entities.User import User



app = Flask(__name__)
csrf=CSRFProtect(app)
app.config['TESTING'] = False

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"


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

 
def conector(a=0 , fechas = 0):
    fecha_actual = datetime.today().strftime('%Y-%m-%d')
    mes_actual = fecha_actual[5:7]
    anio_actual = fecha_actual[0:4]
    cur = db.connection.cursor()
    if(a == 0):
        return 0
    if(a == 1):
        cur.execute("SELECT * FROM registros ORDER BY id DESC")
    if(a == 2):
        cur.execute("SELECT * FROM tarifas WHERE id = '8'")
    if(a == 3):
        cur.execute("SELECT * FROM usuarios_web")
    if(a == 4):
        cur.execute("SELECT * FROM usuarios")
    if(a == 5):
        cur.execute("SELECT * FROM caja_abierta ORDER BY id DESC")
    if(a == 6):
        cur.execute("SELECT * FROM caja_cerradas ORDER BY id DESC")
    if(a==16):
        cur.execute('SELECT * FROM caja_cerradas WHERE SUBSTRING(fecha_cierre,1,10) = (%s);',[fechas])
    if(a == 7):
        cur.execute('SELECT sum(total_recaudado) FROM caja_cerradas WHERE SUBSTRING(fecha_cierre, 1, 10) = (%s);',[fecha_actual])
    if(a == 8):
        cur.execute('SELECT sum(total_recaudado) FROM caja_cerradas WHERE MID(fecha_cierre, 6, 2) = (%s);',[mes_actual])
    if(a == 9):
        cur.execute('SELECT sum(total_recaudado) FROM caja_cerradas WHERE SUBSTRING(fecha_cierre, 1, 4) = (%s);',[anio_actual])
    if(a==10):
         cur.execute('SELECT sum(total_recaudado) FROM caja_cerradas WHERE SUBSTRING(fecha_cierre, 1, 10) = (%s);',[fechas])
    if(a==11):
         cur.execute('SELECT count(*) FROM egreso WHERE fecha_ingreso = (%s);',[fechas])
    if(a==12):
         cur.execute('SELECT count(*) FROM ingreso_diario WHERE fecha_ingreso = (%s);',[fechas])
    if(a==13):
         cur.execute('SELECT count(*) FROM egreso WHERE fecha_egreso = (%s);',[fechas])
    if(a==14):
         cur.execute('SELECT count(*) FROM caja_cerradas WHERE SUBSTRING(fecha_cierre,1,10) = (%s);',[fechas])
    if(a==15):
         cur.execute('SELECT count(*) FROM caja_cerradas WHERE SUBSTRING(fecha_abertura, 1, 10) = (%s);',[fechas])

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
    return render_template("register.html" ,data = conector(3))


@app.route('/registros')
@login_required
def registros():
    return render_template("registros.html" ,  data = conector(1))

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

        

    return render_template("register_siga.html" , data = conector(4))


@app.route('/tarifas_n' , methods = ['GET', 'POST'])
@login_required
def tarifas_n():


    if request.method == "POST":

        cur = db.connection.cursor()

        noacampanteparticular = request.form["particulares_dia"]
        noacampantealumno = request.form["alumno_dia"]
        noacampanteaportante = request.form["aportantes_dia"]
            
        if(noacampanteparticular!=""):
            print("consulto no acampante particular")
            cur.execute('UPDATE tarifas SET particular_d = (%s) WHERE id = 8' , [noacampanteparticular])
        if(noacampantealumno!=""):
            print("consulto no acampante alumno")
            cur.execute('UPDATE tarifas SET alumno_d = (%s) WHERE id = 8' , [noacampantealumno])
        if(noacampanteaportante!=""):
            print("consulto no acampante aportante")
            cur.execute('UPDATE tarifas SET aportante_d = (%s) WHERE id = 8' , [noacampanteaportante])


        db.connection.commit()
    return redirect(url_for("tarifas"))


@app.route('/tarifas_a' , methods = ['GET', 'POST'])
@login_required
def tarifas_a():


    if request.method == "POST":

        cur = db.connection.cursor()

        acampanteparticular = request.form["particulares_acampantes"]
        acampantealumno = request.form["alumnos_acampantes"]
        acampanteaportante = request.form["aportantes_acampantes"]
        if(acampanteparticular!=""):
            cur.execute("UPDATE tarifas SET tarifa_particular = (%s) WHERE id = '8'" , [acampanteparticular])
        if(acampantealumno!=""):
            cur.execute("UPDATE tarifas SET tarifa_alumno = (%s) WHERE id = '8'" , [acampantealumno])
        if(acampanteaportante!=""):
            cur.execute("UPDATE tarifas SET tarifa_aportante = (%s) WHERE id = '8'" , [acampanteaportante])
        db.connection.commit()
    return redirect(url_for("tarifas"))



@app.route('/tarifas')
@login_required
def tarifas():
    return render_template("tarifas.html", tarifa = conector(2))



@app.route('/recaudaciones',  methods = ['GET', 'POST'])
@login_required
def recaudaciones():
    r = []
    c = []
    d = []
    e = []
    caja_a= []
    caja_c = []
    fecha = []
    if request.method =="POST":
        fecha = request.form["fechas"]

        r = conector(10,fecha)
        c = conector(11, fecha)
        d = conector(12, fecha)
        e = conector(13 , fecha)
        caja_a =  conector(14 , fecha)
        caja_c =  conector(15 , fecha)
    return render_template("recaudaciones.html", fecha = fecha , caja_a = conector(5) , caja_c = conector(6) , r_dia = conector(7) , r_mes = conector(8) ,r_anio = conector(9) , r = r , c_p = c, c_pa = d ,c_egresantes = e , cajaa = caja_a, cajac = caja_c)


@app.route('/eliminar' , methods = ['GET', 'POST'])
def eliminar():

    if request.method == "POST":
            cur = db.connection.cursor()
            id = request.form['ID']
            if(id!=""):
                cur.execute('DELETE FROM usuarios WHERE id = (%s)' , [id])
                db.connection.commit()
                flash("Eliminado con exito" , "correcto")
            else:
                flash("Porfavor complete todos los campos con la tabla de abajo.", "error")

    return redirect(url_for("register_siga"))



@app.route('/eliminar_web' , methods = ['GET', 'POST'])
def eliminar_web():


    if request.method == "POST":
            cur = db.connection.cursor()
            usuario = request.form['usuario']
            nombrecomp = request.form['nombrecomp']


            
            if(session['username'] == usuario):
                flash("Error, no se puede eliminar a alguien que este usando el sistema." , "error")
            elif(usuario != "" or nombrecomp != ""):
                cur.execute('DELETE FROM usuarios_web WHERE usuario = (%s) AND nombrecomp = (%s)' , (usuario,nombrecomp))
                db.connection.commit()
                flash("Eliminado con exito" , "correcto")
            else:
                flash("Porfavor complete todos los campos con la tabla de abajo." , "error")
                

    return redirect(url_for("register"))



@app.route('/protected')
@login_required
def protected():
    return "<h1>Esta vista es solo para usuarios.</h1>"

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == "POST": 
        username = request.form['username']
        session['username'] = username
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