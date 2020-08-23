from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask_mysqldb import MySQL

import os
from flask import jsonify
from werkzeug.utils import secure_filename

#coneccion base de datos
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './static'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Mysqlpass123'
app.config['MYSQL_DB'] = 'sancho_Limitada_Data_Base'
base_datos_app = MySQL(app)
#datos del cliente utilizados para el elemento id_relacion_cliente_factura > editar_factura.html
datos_cliente_editar_factura = []
#variable implementada activar/desactivar un producto
desactivar = 0
boton_desactivar_producto_tipo = "btn-primary"
#lista utilizada para el funcionamiento de la api
datos_servidor_factura_json = []
#variables relacionadas con la visualizacion de los formularios y las listas relacionados por cliente-factura-producto
bloque_clientes_estado = "visibility: visible; display: block;"
bloque_facturas_estado = "visibility: hidden; display: none;"
bloque_productos_estado = "visibility: hidden; display: none;"

@app.route('/') 
def index():
    #consultar tablas en la base de datos sql
    consulta_base_datos_cliente = base_datos_app.connection.cursor()
    consulta_base_datos_cliente.execute('SELECT * FROM clientes')
    datos_servidor_cliente = consulta_base_datos_cliente.fetchall()

    consulta_base_datos_factura = base_datos_app.connection.cursor()
    consulta_base_datos_factura.execute('SELECT * FROM facturas')
    datos_servidor_factura = consulta_base_datos_factura.fetchall()

    consulta_base_datos_producto = base_datos_app.connection.cursor()
    consulta_base_datos_producto.execute('SELECT * FROM productos')
    datos_servidor_producto = consulta_base_datos_producto.fetchall()
    #ordenar clientes por cantidda de facturas
    consulta_base_datos_id_cliente_ordendo_factura = base_datos_app.connection.cursor()
    consulta_base_datos_id_cliente_ordendo_factura.execute('SELECT id_relacion_cliente, COUNT(*) FROM facturas GROUP BY id_relacion_cliente ORDER BY COUNT(*) ASC')
    datos_servidor_id_cliente_ordenado_factura = consulta_base_datos_id_cliente_ordendo_factura.fetchall()     
    
    id_cliente_ordenado_factura = []
    for elemento in datos_servidor_id_cliente_ordenado_factura:
        id_cliente_ordenado_factura.append(str(elemento[0]))

    consulta_base_datos_cliente_ordendo_facturax = base_datos_app.connection.cursor()
    cadena_id_cliente_ordenado_factura = ",".join(id_cliente_ordenado_factura)
    if cadena_id_cliente_ordenado_factura == "":
        consulta_base_datos_cliente_ordendo_facturax.execute("SELECT * FROM clientes")
    else:       
        string = "SELECT * FROM clientes ORDER BY FIELD(id_cliente,"+ cadena_id_cliente_ordenado_factura +") DESC"
        consulta_base_datos_cliente_ordendo_facturax.execute(string)

    datos_servidor_cliente_ordenado_factura = consulta_base_datos_cliente_ordendo_facturax.fetchall()
    #activar/desactivar visual productos
    if desactivar == 0:
        productos_activos = []    
        for datos_servidor_producto_activo in datos_servidor_producto:
            if datos_servidor_producto_activo[6] == 'ACTIVO':            
                productos_activos.append(datos_servidor_producto_activo)
        datos_servidor_producto = productos_activos        
    else:
        datos_servidor_producto = datos_servidor_producto

    #datos del cliente utilizados para el elemento id_relacion_cliente_factura > editar_factura.html
    global datos_cliente_editar_factura
    
    datos_cliente_editar_factura = datos_servidor_cliente

    return render_template('index.html', 
                            datos_servidor_cliente = datos_servidor_cliente_ordenado_factura, 
                            datos_servidor_factura = datos_servidor_factura, 
                            datos_servidor_producto = datos_servidor_producto,
                            bloque_clientes = bloque_clientes_estado,
                            bloque_facturas = bloque_facturas_estado,
                            bloque_productos = bloque_productos_estado,
                            boton_desactivar_producto = boton_desactivar_producto_tipo)
#elemento api
@app.route('/api/info_facturas', methods = ['GET']) 
def api():    
    consulta_base_datos = base_datos_app.connection.cursor()
    consulta_base_datos.execute('SELECT * FROM facturas')
    datos_servidor_factura = consulta_base_datos.fetchall()
    global datos_servidor_factura_json
    datos_servidor_factura_json = []
    for elemento in datos_servidor_factura:
        factura = {
            "id_factura" : (elemento[0]),
            "codigo_factura" : (elemento[1]),
            "cliente_compra_factura" : (elemento[2]),
            "producto_factura" : (elemento[3]),
            "cantidad_productos_factura" : (elemento[4]),
            "fecha_compra_factura" : (elemento[5]),
            "valor_total_factura" : (elemento[6]),
            "metodo_pago_factura" : (elemento[7]),
            "id_relacion_cliente" : (elemento[8])
        }
        datos_servidor_factura_json.append(factura)
    return jsonify(datos_servidor_factura_json)
#elemento api
@app.route('/api/info_facturas/codigo/<string:codigo_factura>', methods = ['GET']) 
def api_f(codigo_factura):    
    consulta_base_datos = base_datos_app.connection.cursor()
    consulta_base_datos.execute('SELECT * FROM facturas')
    datos_servidor_factura = consulta_base_datos.fetchall()
    global datos_servidor_factura_json
    datos_servidor_factura_json = []
    for elemento in datos_servidor_factura:
        factura = {
            "id_factura" : (elemento[0]),
            "codigo_factura" : (elemento[1]),
            "cliente_compra_factura" : (elemento[2]),
            "producto_factura" : (elemento[3]),
            "cantidad_productos_factura" : (elemento[4]),
            "fecha_compra_factura" : (elemento[5]),
            "valor_total_factura" : (elemento[6]),
            "metodo_pago_factura" : (elemento[7]),
            "id_relacion_cliente" : (elemento[8])
        }
        datos_servidor_factura_json.append(factura)
    
    consulta = [busqueda_factura for busqueda_factura in datos_servidor_factura_json if busqueda_factura["codigo_factura"] == codigo_factura]
    if len(consulta)>0:
        return jsonify({ "valor_total_factura": consulta[0]['valor_total_factura']})
    else:
        return jsonify({"consulta" : "no se encontro coincidencia"})
#indicador estado para funcion activar/desactivar producto
@app.route('/desactivar', methods = ['POST']) 
def desactivar():    
    global desactivar
    global boton_desactivar_producto_tipo
    if desactivar == 0:
        desactivar = 1
        boton_desactivar_producto_tipo = "btn-secondary"
    else:
        desactivar = 0
        boton_desactivar_producto_tipo = "btn-primary"
    return redirect(url_for('index'))

@app.route('/habilitar_bloque_clientes', methods = ['POST']) 
def habilitar_bloque_clientes():    
    global bloque_clientes_estado
    global bloque_facturas_estado
    global bloque_productos_estado
    bloque_clientes_estado = "visibility: visible; display: block;"
    bloque_facturas_estado = "visibility: hidden; display: none;"
    bloque_productos_estado = "visibility: hidden; display: none;"
    return redirect(url_for('index'))
@app.route('/habilitar_bloque_facturas', methods = ['POST']) 
def habilitar_bloque_facturas():    
    global bloque_clientes_estado
    global bloque_facturas_estado
    global bloque_productos_estado
    bloque_clientes_estado = "visibility: hidden; display: none;"
    bloque_facturas_estado = "visibility: visible; display: block;"
    bloque_productos_estado = "visibility: hidden; display: none;"
    return redirect(url_for('index'))
@app.route('/habilitar_bloque_productos', methods = ['POST']) 
def habilitar_bloque_productos():    
    global bloque_clientes_estado
    global bloque_facturas_estado
    global bloque_productos_estado
    bloque_clientes_estado = "visibility: hidden; display: none;"
    bloque_facturas_estado = "visibility: hidden; display: none;"
    bloque_productos_estado = "visibility: visible; display: block;"
    return redirect(url_for('index'))
    
@app.route('/nuevo_cliente', methods = ['POST']) 
def nuevo_cliente():
    if request.method == 'POST':
        formulario_cedula_cliente = request.form['cedula_cliente']
        formulario_nombre_cliente = request.form['nombre_cliente']
        formulario_direccion_cliente = request.form['direccion_cliente']
        formulario_telefono_cliente = request.form['telefono_cliente']
        #--
        foto_cliente = request.files['foto_cliente']
        nombre_archivo_foto_cliente = secure_filename(foto_cliente.filename)
        if nombre_archivo_foto_cliente == "":
            nada = 1
        else:
            foto_cliente.save(os.path.join(app.config['UPLOAD_FOLDER'], nombre_archivo_foto_cliente))
        #--
        consulta_base_datos = base_datos_app.connection.cursor()
        consulta_base_datos.execute('INSERT INTO clientes (cedula_cliente, nombre_cliente, direccion_cliente, telefono_cliente, foto_cliente) VALUES (%s, %s, %s, %s, %s)'
                                    ,(formulario_cedula_cliente,
                                      formulario_nombre_cliente, 
                                      formulario_direccion_cliente, 
                                      formulario_telefono_cliente, 
                                      (app.config['UPLOAD_FOLDER']+'/'+ nombre_archivo_foto_cliente)))
        base_datos_app.connection.commit()
        return redirect(url_for('index'))

@app.route('/nueva_factura', methods = ['POST']) 
def nueva_factura():
    if request.method == 'POST':
        formulario_codigo_factura = request.form['codigo_factura']
        formulario_cliente_compra_factura = request.form['cliente_compra_factura']
        formulario_fecha_factura = request.form['fecha_factura']
        formulario_metodo_pago_factura = request.form['metodo_pago_factura']
        formulario_id_relacion_cliente_factura = request.form['id_relacion_cliente_factura']
                
        consulta_base_datos = base_datos_app.connection.cursor()
        consulta_base_datos.execute('SELECT * FROM productos')
        datos_servidor_producto = consulta_base_datos.fetchall()

        #crear cadena con el nombre de los productos en la factura y la cantidad total de productos
        cadena_cantidades_productos = ''
        cantidad_total_productos = 0
        precio_total_productos = 0
        for elemento in datos_servidor_producto:
            cantidad_total_productos += int(request.form[str(elemento[0])])
            precio_total_productos += (int(elemento[4])*int(request.form[str(elemento[0])]))
            if request.form[str(elemento[0])] == '0':
                nada = 1
            else:
                cadena_cantidades_productos += ',' + str(elemento[3])
                
        consulta_base_datos.execute('INSERT INTO facturas (codigo_factura, cliente_compra_factura, productos_factura, cantidad_productos_factura, fecha_compra_factura, valor_total_factura, metodo_pago_factura, id_relacion_cliente) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
                                    ,(formulario_codigo_factura
                                    ,formulario_cliente_compra_factura
                                    ,cadena_cantidades_productos
                                    ,cantidad_total_productos
                                    ,formulario_fecha_factura
                                    ,precio_total_productos
                                    ,formulario_metodo_pago_factura
                                    ,formulario_id_relacion_cliente_factura))
        base_datos_app.connection.commit()
        
        return redirect(url_for('index'))

@app.route('/nuevo_producto', methods = ['POST']) 
def nuevo_producto():
    if request.method == 'POST':
        formulario_codigo_producto = request.form['codigo_producto']
        formulario_categoria_producto = request.form['categoria_producto']
        formulario_nombre_producto = request.form['nombre_producto']
        formulario_precio_producto = request.form['precio_producto']
        formulario_cantidad_bodega_producto = request.form['cantidad_bodega_producto']
        formulario_estado_producto = request.form['estado_producto']
        if formulario_precio_producto == "":
            formulario_precio_producto = 0
        else:
            nada = 1
        if formulario_cantidad_bodega_producto == "":
            formulario_cantidad_bodega_producto = "0"
        else:
            nada = 1
        consulta_base_datos = base_datos_app.connection.cursor()
        consulta_base_datos.execute('INSERT INTO productos (codigo_producto, categoria_producto, nombre_producto, precio_producto, cantidad_bodega_producto, estado_producto) VALUES (%s, %s, %s, %s, %s, %s)'
                                    ,(formulario_codigo_producto,
                                    formulario_categoria_producto,
                                    formulario_nombre_producto,
                                    formulario_precio_producto,
                                    formulario_cantidad_bodega_producto,
                                    formulario_estado_producto))
        base_datos_app.connection.commit()
        return redirect(url_for('index'))

@app.route('/borrar_cliente/<id_cliente>') 
def borrar_cliente(id_cliente):
    consulta_base_datos = base_datos_app.connection.cursor()
    consulta_base_datos.execute('DELETE FROM clientes WHERE id_cliente = {0}'.format(id_cliente))
    base_datos_app.connection.commit()
    
    return redirect(url_for('index'))

@app.route('/editar_cliente/<id_cliente>') 
def editar_cliente(id_cliente):
    consulta_base_datos = base_datos_app.connection.cursor()
    consulta_base_datos.execute('SELECT * FROM clientes WHERE id_cliente = {0}'.format(id_cliente))
    datos_servidor_cliente_editar = consulta_base_datos.fetchall()
    return render_template('editar_cliente.html', datos_servidor_cliente_editar = datos_servidor_cliente_editar[0])

@app.route('/actualizar_cliente/<id_cliente>', methods = ['POST']) 
def actualizar_cliente(id_cliente):
    if request.method == 'POST':
        formulario_cedula_cliente = request.form['cedula_cliente']
        formulario_nombre_cliente = request.form['nombre_cliente']
        formulario_direccion_cliente = request.form['direccion_cliente']
        formulario_telefono_cliente = request.form['telefono_cliente']
        
        #--
        foto_cliente = request.files['foto_cliente']
        nombre_archivo_foto_cliente = secure_filename(foto_cliente.filename)
        if nombre_archivo_foto_cliente == "":
            nada = 1
        else:
            foto_cliente.save(os.path.join(app.config['UPLOAD_FOLDER'], nombre_archivo_foto_cliente))
        #--

        consulta_base_datos = base_datos_app.connection.cursor()
        consulta_base_datos.execute('''
                                    UPDATE clientes 
                                    SET cedula_cliente = %s,
                                        nombre_cliente = %s,
                                        direccion_cliente = %s,
                                        telefono_cliente = %s,
                                        foto_cliente = %s
                                    WHERE id_cliente = %s                                    
                                    '''
                                    ,(formulario_cedula_cliente
                                    ,formulario_nombre_cliente
                                    ,formulario_direccion_cliente
                                    ,formulario_telefono_cliente
                                    ,(app.config['UPLOAD_FOLDER']+'/'+ nombre_archivo_foto_cliente)
                                    ,id_cliente))
        base_datos_app.connection.commit()
        return redirect(url_for('index'))

@app.route('/editar_factura/<id_factura>')         
def editar_factura(id_factura):
    consulta_base_datos = base_datos_app.connection.cursor()
    consulta_base_datos.execute('SELECT * FROM facturas WHERE id_factura = {0}'.format(id_factura))
    #elemento utilizado para asignar el id de los usarios disponibles al elemento id_relacion_cliente_factura > editar_factura.html
    datos_servidor_factura_editar = consulta_base_datos.fetchall()

    consulta_base_datos.execute('SELECT * FROM productos')
    datos_servidor_producto = consulta_base_datos.fetchall()

    return render_template('editar_factura.html', datos_servidor_factura_editar = datos_servidor_factura_editar[0],
                                                  datos_cliente_editar_factura = datos_cliente_editar_factura, 
                                                  datos_servidor_producto=datos_servidor_producto)

@app.route('/actualizar_factura/<id_factura>', methods = ['POST']) 
def actualizar_factura(id_factura):
    if request.method == 'POST':
        formulario_codigo_factura = request.form['codigo_factura']
        formulario_cliente_compra_factura = request.form['cliente_compra_factura']
        formulario_fecha_factura = request.form['fecha_factura']
        formulario_metodo_pago_factura = request.form['metodo_pago_factura']
        formulario_id_relacion_cliente_factura = request.form['id_relacion_cliente_factura']

        consulta_base_datos = base_datos_app.connection.cursor()

        #crear cadena con el nombre de los productos en la factura y la cantidad total de productos
        consulta_base_datos.execute('SELECT * FROM productos')
        datos_servidor_producto = consulta_base_datos.fetchall()        
        cadena_cantidades_productos = ''
        cantidad_total_productos = 0
        precio_total_productos = 0
        for elemento in datos_servidor_producto:
            cantidad_total_productos += int(request.form[str(elemento[0])])
            precio_total_productos += (int(elemento[4])*int(request.form[str(elemento[0])]))
            if request.form[str(elemento[0])] == '0':
                nada = 1
            else:
                cadena_cantidades_productos += ',' + str(elemento[3])
        
        consulta_base_datos.execute('''
                                    UPDATE facturas 
                                    SET codigo_factura = %s,
                                    cliente_compra_factura = %s,
                                    productos_factura = %s,
                                    cantidad_productos_factura = %s,
                                    fecha_compra_factura = %s,
                                    valor_total_factura = %s,
                                    metodo_pago_factura = %s,
                                    id_relacion_cliente = %s
                                    WHERE id_factura = %s                                   
                                    '''
                                    ,(formulario_codigo_factura
                                    ,formulario_cliente_compra_factura
                                    ,cadena_cantidades_productos
                                    ,cantidad_total_productos
                                    ,formulario_fecha_factura
                                    ,precio_total_productos
                                    ,formulario_metodo_pago_factura
                                    ,formulario_id_relacion_cliente_factura
                                    ,id_factura))
        base_datos_app.connection.commit()
        return redirect(url_for('index'))

@app.route('/editar_producto/<id_producto>') 
def editar_producto(id_producto):
    consulta_base_datos = base_datos_app.connection.cursor()
    consulta_base_datos.execute('SELECT * FROM productos WHERE id_producto = {0}'.format(id_producto))
    datos_servidor_producto_editar = consulta_base_datos.fetchall()
    return render_template('editar_producto.html', datos_servidor_producto_editar = datos_servidor_producto_editar[0])

@app.route('/actualizar_producto/<id_producto>', methods = ['POST']) 
def actualizar_producto(id_producto):
    if request.method == 'POST':
        formulario_codigo_producto = request.form['codigo_producto']
        formulario_categoria_producto = request.form['categoria_producto']
        formulario_nombre_producto = request.form['nombre_producto']
        formulario_precio_producto = request.form['precio_producto']
        formulario_cantidad_bodega_producto = request.form['cantidad_bodega_producto']
        formulario_estado_producto = request.form['estado_producto']

        consulta_base_datos = base_datos_app.connection.cursor()
        consulta_base_datos.execute('''
                                    UPDATE productos
                                    SET codigo_producto = %s,
                                    categoria_producto = %s,
                                    nombre_producto = %s,
                                    precio_producto = %s,
                                    cantidad_bodega_producto = %s,
                                    estado_producto = %s
                                    WHERE id_producto = %s                                    
                                    '''
                                    ,(formulario_codigo_producto,
                                    formulario_categoria_producto,
                                    formulario_nombre_producto,
                                    formulario_precio_producto,
                                    formulario_cantidad_bodega_producto,
                                    formulario_estado_producto,
                                    id_producto))
        base_datos_app.connection.commit()
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(port = 5000, debug = True)

