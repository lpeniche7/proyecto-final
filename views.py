import functools
from formularios import formularioMensaje
from flask import Flask, render_template, blueprints, request, redirect, url_for,session, flash, send_file
from werkzeug.security import check_password_hash, generate_password_hash
from db import get_db




main= blueprints.Blueprint('main', __name__)


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'usuario' not in session:
            return redirect(url_for('main.login'))
        return view(**kwargs)

    return wrapped_view

#Inicio de seccion,login y Registro*****

@main.route( '/' )
def hello_world():
    """Función que maneja la raiz del sitio web.

        Parameters:
        Ninguno

        Returns:
        Plantilla inicio.html

    """

    return render_template('inicio.html')


@main.route('/login/', methods=['GET', 'POST'])
def login():
    """Función que maneja la ruta login.Responde a los métodos GET y POST.

        Parameters:
        Ninguno

        Returns:
        login.html si es invocada con el método GET. 
        Redirecciona a  main.ajax si es invocada con POST y la validación es verdadera.

    """

    if request.method =='POST':

        usuario = request.form['username']
        clave = request.form['userPassword']
        db = get_db()
        #sql = "select * from usuario where usuario = '{0}' and clave= '{1}'".format(usuario, clave)

        user = db.execute('select * from usuario where username = ? ', (usuario,)).fetchone()
        db.commit()
        db.close()
        if user is not None:

            #print(user[4])
            clave = clave + usuario
            
            sw = check_password_hash(user[4], clave)

            if(sw):

                session['nombre'] = user[1]
                session['usuario'] = user[2]
                if user[5] == 0:
                 return redirect(url_for('main.DashboardSuper'))
                elif  user[5] == 1:
                 return redirect(url_for('main.DashboardPiloto'))   
                elif  user[5] == 2:
                 return redirect(url_for('main.DashboardPasajero')) 

        flash('Usuario o clave incorrecto.')
    
    return render_template('login.html')


@main.route('/registro/', methods=['GET', 'POST'])
def registro():
    """Función que maneja la ruta Registro.Responde a los métodos GET y POST.

        Parameters:
        Ninguno

        Returns:
        registro.html si es invocada con el método GET. 
        Crea un usuario en la BD si es invocada con POST, no tiene válidaciones.

    """
   
    if request.method == 'POST' :

        nombre = request.form['nombre']
        usuario = request.form['username']
        correo = request.form['correo']
        clave = request.form['contraseña']
        t_user = "2"
        

        db = get_db()
        #agregar SLAT
        clave = clave + usuario
        clave = generate_password_hash(clave)
        db.execute("insert into usuario ( nombre, username, correo, clave, tipo_user) values( ?, ?, ?, ?, ?)",(nombre, usuario, correo, clave, t_user))
        db.commit()
        db.close()
        flash('Cuenta Creada')
        return redirect(url_for('main.registro'))

    elif  request.method == 'GET':       
        
       return render_template('registro.html')


#******Superusuario********


@main.route('/DashboardSuper/')
@login_required
def DashboardSuper():
    return render_template('DashboardSuper.html')

#********Menu Usuarios********


@main.route('/DashboardSuperUsers/', methods=['GET', 'POST'])
@login_required
def DashboardSuperUsers():
     
    if request.method == 'POST' :

        nombre = request.form['nombre']
        usuario = request.form['username']
        correo = request.form['correo']
        clave = request.form['clave']
        t_user = request.form['tipo_user']
        

        db = get_db()
        #agregar SLAT
        clave = clave + usuario
        clave = generate_password_hash(clave)
        db.execute("insert into usuario ( nombre, username, correo, clave, tipo_user) values( ?, ?, ?, ?, ?)",(nombre, usuario, correo, clave, t_user))
        db.commit()
        db.close()
        flash('Cuenta Creada')
        return redirect(url_for('main.DashboardSuperUsers'))



    elif  request.method == 'GET':       
      
      try:
        datos =[]
        db= get_db()
        cursor= db.cursor()
        sql="SELECT * from  usuario,tipo_usuario where usuario.tipo_user= tipo_usuario.id;"
        cursor.execute(sql)
        datos = cursor.fetchall()
        db.commit()
        db.close()
  
      except Exception as ex:
        return print("mensaje error")        
    
    return render_template('DashboardSuperUsers.html', usuarios = datos)

@main.route('/DashboardSuperUsersDelete/<string:username>')
@login_required
def DashboardSuperUsersDelete(username):
        
    try:
        db= get_db()
        cursor= db.cursor()
       
        cursor.execute('DELETE from usuario where usuario.username = ? ', (username,)).fetchone
        db.commit()
        db.close()
        
            
    except Exception as ex:
        return print("mensaje error")        
    
    return redirect(url_for('main.DashboardSuperUsers'))

@main.route('/DashboardSuperUsersEdit/<id>', methods=['GET','POST'])
@login_required
def get_contact(id):
    db= get_db()
    cursor= db.cursor() 
    cursor.execute('SELECT * from usuario where id = ? ', (id,))
    data=cursor.fetchall()
    db.commit()
    db.close()
    #print(data)
    return  render_template('DashboardSuperUsersUpdate.html', usuario = data[0])
    


@main.route('/DashboardSuperUsersUpdate/', methods=['POST','GET'])
@login_required
def DashboardSuperUsersUpdate():
    if request.method == 'POST':
     id= request.form['id']
     nombre = request.form['nombre']
     usuario = request.form['username']
     correo = request.form['correo']
     clave = request.form['clave']
     t_user = request.form['tipo_user']
     db = get_db()
     #agregar SLAT
     clave = clave + usuario
     clave = generate_password_hash(clave)
     db.execute("UPDATE usuario SET(nombre, username, correo, clave, tipo_user) values( ?, ?, ?, ?, ?, ?)",(nombre, usuario, correo, clave, t_user))
            
     db.commit()
     db.close()
     flash('Cuenta Actualizada')
     return redirect(url_for('main.DashboardSuperUsersEdit'))

#****Menu Vuelos********

@main.route('/DashboardSuperVuelos/', methods=['GET', 'POST'])
@login_required
def DashboardSuperVuelos():
     
    if request.method == 'POST' :
        
        fecha = request.form['fecha']
        hora = request.form['hora']
        origen = request.form['origen']
        destino = request.form['destino']
        piloto = request.form['id_piloto']
        avion= request.form['avion']
        capacidad=request.form['capacidad']
        estado=request.form['estado']

        db = get_db()
                  # "insert into usuario ( nombre, username, correo, clave, tipo_user) values( ?, ?, ?, ?, ?)",(nombre, usuario, correo, clave, t_user))
        db.execute("insert into vuelos ( fecha, hora, c_origen, c_destino, t_piloto, avion, capacidad, t_estados) values( ?, ?, ?, ?, ?, ?, ?, ?)",(fecha, hora, origen, destino, piloto, avion, capacidad, estado))
        db.commit()
        db.close()
        flash('Cuenta Creada')
        return redirect(url_for('main.DashboardSuperVuelos'))



    elif  request.method == 'GET':       
      
      try:
        datos =[]
        db= get_db()
        cursor= db.cursor()
        sql="Select fecha,hora,c_origen,c_destino,usuario.nombre as piloto,avion,capacidad,estados.nombre As Estado from usuario,vuelos,estados where vuelos.t_piloto=usuario.id and vuelos.t_estados=estados.id;"
        cursor.execute(sql)
        dvuelo = cursor.fetchall()
        print(dvuelo)
        
  
      except Exception as ex:
        return print("mensaje error")        
    
    return render_template('DashboardSuperVuelos.html', vuelos = dvuelo)
"""
@main.route('/DashboardSuperVuelosDelete/<id>')
@login_required
def DashboardSuperVuelosDelete(id):
        
    try:
        db= get_db()
        cursor= db.cursor()
       
        cursor.execute('DELETE from vuelos where vuelos.id = ? ', (id,)).fetchone
        db.commit()
        db.close()
        
            
    except Exception as ex:
        return print("mensaje error")        
    
    return redirect(url_for('main.DashboardSuperVuelos'))

@main.route('/DashboardSuperUsersEdit/<id>', methods=['GET','POST'])
@login_required
def get_contact(id):
    db= get_db()
    cursor= db.cursor() 
    cursor.execute('SELECT * from usuario where id = ? ', (id,))
    data=cursor.fetchall()
    db.commit()
    db.close()
    #print(data)
    return  render_template('DashboardSuperUsersUpdate.html', usuario = data[0])
    


@main.route('/DashboardSuperUsersUpdate/', methods=['POST','GET'])
@login_required
def DashboardSuperUsersUpdate():
    if request.method == 'POST':
     id= request.form['id']
     nombre = request.form['nombre']
     usuario = request.form['username']
     correo = request.form['correo']
     clave = request.form['clave']
     t_user = request.form['tipo_user']
     db = get_db()
     #agregar SLAT
     clave = clave + usuario
     clave = generate_password_hash(clave)
     db.execute("UPDATE usuario SET(nombre, username, correo, clave, tipo_user) values( ?, ?, ?, ?, ?, ?)",(nombre, usuario, correo, clave, t_user))
            
     db.commit()
     db.close()
     flash('Cuenta Actualizada')
     return redirect(url_for('main.DashboardSuperUsersEdit'))

"""
    
#/DashboardSuperVuelosEdit/    

#***********Menu Reserva********
@main.route('/DashboardSuperReserva/', methods=['GET', 'POST'])
@login_required
def DashboardSuperReserva():
     
    if request.method == 'POST' :

        nombre = request.form['nombre']
        usuario = request.form['username']
        correo = request.form['correo']
        clave = request.form['clave']
        t_user = request.form['tipo_user']
        

        db = get_db()
        #agregar SLAT
        clave = clave + usuario
        clave = generate_password_hash(clave)
        db.execute("insert into usuario ( nombre, username, correo, clave, tipo_user) values( ?, ?, ?, ?, ?)",(nombre, usuario, correo, clave, t_user))
        db.commit()
        db.close()
        flash('Cuenta Creada')
        return redirect(url_for('main.DashboardSuperReserva'))



    elif  request.method == 'GET':       
      
      try:
        datos =[]
        db= get_db()
        cursor= db.cursor()
        sql="select vuelos.c_origen,vuelos.c_destino,vuelos.capacidad,vuelos.fecha,reserva.f_reserva,reserva.h_reserva,usuario.nombre  from vuelos,reserva,usuario where reserva.tipo_vuelo=vuelos.id and usuario.id =reserva.u_reserva;"
        cursor.execute(sql)
        dreserva = cursor.fetchall()
        db.commit()
        db.close()
        
        
  
      except Exception as ex:
        return print("mensaje error")        
    print(dreserva)
    return render_template('DashboardSuperReserva.html', reservas = dreserva)

@main.route('/DashboardSuperValoracion/', methods=['GET', 'POST'])
@login_required
def DashboardSuperValoracion():
     
    if request.method == 'POST' :

        nombre = request.form['nombre']
        usuario = request.form['username']
        correo = request.form['correo']
        clave = request.form['clave']
        t_user = request.form['tipo_user']
        

        db = get_db()
        #agregar SLAT
        clave = clave + usuario
        clave = generate_password_hash(clave)
        db.execute("insert into usuario ( nombre, username, correo, clave, tipo_user) values( ?, ?, ?, ?, ?)",(nombre, usuario, correo, clave, t_user))
        db.commit()
        db.close()
        flash('Cuenta Creada')
        return redirect(url_for('main.DashboardSuperValoracion'))



    elif  request.method == 'GET':       
      
      try:
        datos =[]
        db= get_db()
        cursor= db.cursor()
        sql="select vuelos.c_origen,vuelos.c_destino,vuelos.capacidad,vuelos.fecha,reserva.f_reserva,reserva.h_reserva,usuario.nombre  from vuelos,reserva,usuario where reserva.tipo_vuelo=vuelos.id and usuario.id =reserva.u_reserva;"
        cursor.execute(sql)
        dreserva = cursor.fetchall()
        db.commit()
        db.close()
        
        
  
      except Exception as ex:
        return print("mensaje error")        
    print(dreserva)
    return render_template('DashboardSuperValoracion.html', reservas = dreserva)






#***********Menu Valoracion********


#*******Piloto******

@main.route('/DashboardPiloto/')
@login_required
def DashboardPiloto():

    return render_template('DashboardPiloto.html')

@main.route('/DashboardPilotoVuelos/', methods=['GET', 'POST'])
@login_required
def DashboardPilotoVuelos():
     
    if request.method == 'POST' :
        
        fecha = request.form['fecha']
        hora = request.form['hora']
        origen = request.form['origen']
        destino = request.form['destino']
        piloto = request.form['id_piloto']
        avion= request.form['avion']
        capacidad=request.form['capacidad']
        estado=request.form['estado']

        db = get_db()
                  # "insert into usuario ( nombre, username, correo, clave, tipo_user) values( ?, ?, ?, ?, ?)",(nombre, usuario, correo, clave, t_user))
        db.execute("insert into vuelos ( fecha, hora, c_origen, c_destino, t_piloto, avion, capacidad, t_estados) values( ?, ?, ?, ?, ?, ?, ?, ?)",(fecha, hora, origen, destino, piloto, avion, capacidad, estado))
        db.commit()
        db.close()
        flash('Cuenta Creada')
        return redirect(url_for('main.DashboardPilotoVuelos'))



    elif  request.method == 'GET':       
      
      try:
        datos =[]
        db= get_db()
        cursor= db.cursor()
        sql="Select fecha,hora,c_origen,c_destino,usuario.nombre as piloto,avion,capacidad,estados.nombre As Estado from usuario,vuelos,estados where vuelos.t_piloto=usuario.id and vuelos.t_estados=estados.id;"
        cursor.execute(sql)
        dvuelo = cursor.fetchall()
        print(dvuelo)
        
  
      except Exception as ex:
        return print("mensaje error")        
    
    return render_template('DashboardPilotoVuelos.html', vuelos = dvuelo)







#******Pasasjero******

@main.route('/DashboardPasajero/')
@login_required
def DashboardPasajero():

    return render_template('DashboardPasajero.html')


@main.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.login'))





