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

def registros_db(a = 0, fechas = 0, usuarios = 0):
    cur = db.connection.cursor()
    if(a == 0 or fechas == 0 or fechas == 0):
        return 0
    if(a == 1):
        cur.execute('SELECT count(*) FROM registros WHERE fecha = (%s) AND usuario = (%s) AND comentario = "ha ingresado un nuevo particular acampante";',(fechas ,usuarios))
    if(a == 2):
        cur.execute('SELECT count(*) FROM registros WHERE fecha = (%s) AND usuario = (%s) AND comentario = "ha ingresado un nuevo particular por el dia";',(fechas ,usuarios))
    if(a == 3):
        cur.execute('SELECT count(*) FROM registros WHERE fecha = (%s) AND usuario = (%s) AND comentario = "ha ingresado un nuevo alumno acampante";',(fechas ,usuarios))
    if(a == 4):
        cur.execute('SELECT count(*) FROM registros WHERE fecha = (%s) AND usuario = (%s) AND comentario = "ha ingresado un nuevo alumno por el dia";',(fechas ,usuarios))
    if(a == 5):
        cur.execute('SELECT count(*) FROM registros WHERE fecha = (%s) AND usuario = (%s) AND comentario = "ha ingresado un nuevo aportante acampante";',(fechas ,usuarios))
    if(a == 6):
        cur.execute('SELECT count(*) FROM registros WHERE fecha = (%s) AND usuario = (%s) AND comentario = "ha ingresado un nuevo aportante por el dia";',(fechas ,usuarios))
   
    if(a == 7):
        cur.execute('SELECT count(*) FROM registros WHERE fecha = (%s) AND comentario = "ha ingresado un nuevo particular acampante";',([fechas]))
    if(a == 8):
        cur.execute('SELECT count(*) FROM registros WHERE fecha = (%s) AND comentario = "ha ingresado un nuevo particular por el dia";',([fechas]))
    if(a == 9):
        cur.execute('SELECT count(*) FROM registros WHERE fecha = (%s) AND comentario = "ha ingresado un nuevo alumno acampante";',([fechas]))
    if(a == 10):
        cur.execute('SELECT count(*) FROM registros WHERE fecha = (%s) AND comentario = "ha ingresado un nuevo alumno por el dia";',([fechas]))
    if(a == 11):
        cur.execute('SELECT count(*) FROM registros WHERE fecha = (%s) AND comentario = "ha ingresado un nuevo aportante acampante";',([fechas]))
    if(a == 12):
        cur.execute('SELECT count(*) FROM registros WHERE fecha = (%s) AND comentario = "ha ingresado un nuevo aportante por el dia";',([fechas]))
    

     #   aportante_noacampante = registros_db(6,fecha,usuario)
   
    return cur.fetchall()



def conector(a=0 , fechas = 0 , usuarios = 0):
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
    if(a == 21):
        cur.execute("SELECT privilegios FROM usuarios WHERE usuario  = (%s);",[usuarios])
    if(a == 17):
        cur.execute("SELECT count(*) FROM ingreso")
    if(a == 18):
        cur.execute("SELECT count(*) FROM ingreso_diario")
    if(a == 19):
        cur.execute('SELECT count(*) FROM registros WHERE fecha = (%s) AND usuario = (%s);',(fechas ,usuarios))
    if(a == 5):
        cur.execute("SELECT * FROM caja_abierta ORDER BY id DESC")
    if(a == 6):
        cur.execute("SELECT * FROM caja_cerradas ORDER BY id DESC")
    if(a == 22):
        cur.execute("SELECT * FROM caja_cerradas WHERE SUBSTRING(fecha_cierre, 1, 10) = (%s) ORDER BY id DESC", [fechas])
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
    if(a==20):
        cur.execute('SELECT sum(total_recaudado) FROM caja_cerradas WHERE SUBSTRING(fecha_cierre, 1, 10) = (%s) AND usuario = (%s)',(fechas,usuarios))

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


    return render_template('index.html', data = conector(1), tarifa = conector(2), cantidadacm = conector(17), cantidadd = conector(18))

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
    users = conector(4)
    total = []
    privilegios = []
    r = []
    c = []
    d = []
    e = []
    caja_a= []
    caja_c = []
    fecha = []
    usuario = []
    g = []
    cajas_cerradas_por_fecha = []
    particular_acampantes = []
    particular_noacampantes = []

    alumno_acampante = []
    alumno_noacampante = []

    aportante_acampante = []
    aportante_noacampante = []

    particular_acampantes_tot = []
    particular_noacampantes_tot = []

    alumno_acampante_tot = []
    alumno_noacampante_tot = []

    aportante_acampante_tot = []
    aportante_noacampante_tot = []
    if request.method =="POST":
        fecha = request.form["fechas"]
        usuario = request.form["usuario"]
        
        r = conector(10,fecha)
        c = conector(11, fecha)
        d = conector(12, fecha)
        e = conector(13 , fecha)
        g = conector(20 , fecha, usuario)
        caja_a =  conector(14 , fecha)
        caja_c =  conector(15 , fecha)
        privilegios = conector(21 ,0 , usuario)
        total = conector(19, fecha, usuario)
        particular_acampantes = registros_db(1,fecha,usuario)
        particular_noacampantes = registros_db(2,fecha,usuario)

        alumno_acampante = registros_db(3,fecha,usuario)
        alumno_noacampante = registros_db(4,fecha,usuario)

        aportante_acampante = registros_db(5,fecha,usuario)
        aportante_noacampante = registros_db(6,fecha,usuario)


        particular_acampantes_tot = registros_db(7,fecha)
        particular_noacampantes_tot = registros_db(8,fecha)

        alumno_acampante_tot = registros_db(9,fecha)
        alumno_noacampante_tot = registros_db(10,fecha)

        aportante_acampante_tot = registros_db(11,fecha)
        aportante_noacampante_tot = registros_db(12,fecha)

        cajas_cerradas_por_fecha = conector(22, fecha)

    return render_template("recaudaciones.html", 
    fecha = fecha , caja_a = conector(5) , caja_c = conector(6)
     , r_dia = conector(7) , r_mes = conector(8) , r_anio = conector(9) 
     , r = r , c_p = c, c_pa = d 
     , c_egresantes = e ,cajaa = caja_a
     , cajac = caja_c,  t = total 
     , u = users, p = usuario
     , a1 = particular_acampantes , b1 = particular_noacampantes , c1 = alumno_acampante , d1 = alumno_noacampante , e1 = aportante_acampante , f1 = aportante_noacampante
     , recaudado_u = g
     ,ppp = privilegios
     , cajas_cerradas_por_f = cajas_cerradas_por_fecha
     ,b2 = particular_acampantes_tot
     ,b3 = particular_noacampantes_tot
     ,b4 = alumno_acampante_tot 
     ,b5 =  alumno_noacampante_tot
     ,b6 =  aportante_acampante_tot 
     ,b7 =  aportante_noacampante_tot 
  #   ,cantidadacm = conector(17), cantidadd = conector(18)
     ) 

  
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