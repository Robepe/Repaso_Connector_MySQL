import mysql.connector
from datetime import datetime
import Color


# Metodo que devuelve la Fecha y la Hora local
def setFecha():
	now = datetime.now() 				#almacenamos una variable de tipo 'datetime'

	fecha = now.strftime("%d/%m/%Y")	#proporcionamos un formato a la fecha
	hora = now.strftime("%H:%M:%S")		#proporcionamos un formato a la hora

	return fecha, hora					# retornamos la fecha y la hora formateadas


# Metodo de tipo 'bool' destinado a comprobar una seleccion de tipo (S/N)
def confirmarOperacion():
	while True:
		opcion = (str(input().strip().lower()))
		if (opcion == "s"):				# de ser 's' o 'S', retornamos True
			return True
		elif (opcion == "n"):			# de ser 'n' o 'N', retornamos False
			return False
		else:
			print("\nOperacion no reconocida")	# de no estar contemplada la respuesta, reiniciamos el bucle


# Metodo que recoge un String y valida tanto la longitud como la presencia de caracteres no deseados
def validarString(string):
	y = string.strip()
	for intento in range(5):
		if ((len(y) < 1) or (len(y) > 40)):
			print("\nEntrada invalida: minimo un caracter, maximo 20 caracteres\nPruebe de nuevo:")
			y = str(input()).strip()
		else:
			return y

	print("-" * 20, "Operacion Cancelada", "-" * 20)
	return False

#Método que recoge un String, para eliminar caracteres en blanco, y lo convierte a un Integer
def validarInteger(x):
	for intento in range(5):
		y = x.strip()	# eliminamos los posibles espacios vacios al inicio y final
		try:
			z = int(y)	# tratamos de castear el valor proporcionado a la variable 'z'
			return z	# de ser posible, se retorna la variable 'z'
		except ValueError:
			print("\nEntrada no valida: introduzca exclusivamente numeros entre 0 y 9:\n")
			x = input()	# de no serlo, volvemos a pedir una cifra
	
	print("\nOperacion cancelada\n")


def ConectarDB():
	conn = mysql.connector.connect(user='root', password='', host='localhost')
	return conn


def DesconectarDB(conn):
	conn.close()


def crearDatabase(conn):
	cursor = conn.cursor()

	cursor.execute('''CREATE DATABASE IF NOT EXISTS Ejercicio2''')
	cursor.execute('''USE Ejercicio2''')
	print("Database created successfully")
	
	cursor.close()


def crearTabla(conn):
	cursor = conn.cursor()

	cursor.execute('''CREATE TABLE IF NOT EXISTS cliente 
			(clienteID INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
			 nombre VARCHAR(20) NOT NULL)''')

	cursor.execute('''CREATE TABLE IF NOT EXISTS empresa 
			(empresaID INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
			 nombre VARCHAR(20) NOT NULL)''')

	cursor.execute('''CREATE TABLE IF NOT EXISTS pedido 
			(pedidoID INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
			 nombre VARCHAR(20) NOT NULL,
			 clienteID INT NOT NULL,
			 empresaID INT NOT NULL,
			 FOREIGN KEY (clienteID) REFERENCES cliente (clienteID),
			 FOREIGN KEY (empresaID) REFERENCES empresa (empresaID))''')

	print("Tables created successfully")
	cursor.close()


def insertarCliente(conn):
	cursor = conn.cursor()
	fin = False
	while(not fin):
		print("Introduzca el nombre: ")
		nombre = validarString(str(input()))

		print(Color.WHITE,"\n\tNombre: " + nombre,Color.END,
		"\n\n¿Desea añadir a la persona? (S/N)")

		confirmacion = confirmarOperacion()
		if confirmacion:
			cursor.execute("INSERT INTO cliente (nombre) \
				VALUES ('" + nombre +"')")
			
			print(Color.GREEN,"Cliente añadido correctamente",Color.END)
			conn.commit()
		else:
			print("\nOperación cancelada")

		print("\n¿Desea añadir otro cliente? (S/N)")
		answer = confirmarOperacion()
		if not answer:
			fin = True
			cursor.close()

def insertarEmpresa(conn):
	cursor = conn.cursor()
	fin = False
	while(not fin):
		print("Introduzca el nombre: ")
		nombre = validarString(str(input()))

		print(Color.WHITE,"\n\tNombre: " + nombre,Color.END,
		"\n\n¿Desea añadir a la Empresa? (S/N)")

		confirmacion = confirmarOperacion()
		if confirmacion:
			cursor.execute("INSERT INTO empresa (nombre) \
				VALUES ('" + nombre +"')")
			
			print(Color.GREEN,"Empresa añadida correctamente",Color.END)
			conn.commit()
		else:
			print("\nOperación cancelada")

		print("\n¿Desea añadir otra Empresa? (S/N)")
		answer = confirmarOperacion()
		if not answer:
			fin = True
			cursor.close()


def insertarPedido(conn):
	cursor = conn.cursor()
	fin = False
	while(not fin):
		print("Introduzca el nombre: ")
		nombre = validarString(str(input()))
		print("Introduzca el ID del Cliente: ")
		clienteID = validarString(str(input()))
		print("Introduzca el ID de la empresa: ")
		empresaID = str(validarInteger(str(input())))

		print(Color.WHITE,"\n\tNombre: " + nombre + "\n\tClienteID: " + clienteID + "\n\tempresaID: " + empresaID, Color.END,
		"\n\n¿Desea añadir el pedido? (S/N)")

		confirmacion = confirmarOperacion()
		if confirmacion:
			cursor.execute("INSERT INTO pedido (nombre,clienteID,empresaID) \
				VALUES ('" + nombre +"', '" + clienteID + "', '" + empresaID + "')")
			
			print(Color.GREEN,"Persona añadida correctamente",Color.END)
			conn.commit()
		else:
			print("\nOperación cancelada")

		print("\n¿Desea añadir otro pedido? (S/N)")
		answer = confirmarOperacion()
		if not answer:
			fin = True
			cursor.close()


def mostrarClientes(conn):
	print("\t-- Mostrar Clientes --")
	cursor = conn.cursor()

	cursor.execute("SELECT * FROM cliente")	
	for row in cursor:
		print(Color.WHITE)
		print("\tID = ", row[0], "\n\tNombre = ", row[1],"\n",Color.END)

	print("-" * 40)
	cursor.close()


def mostrarEmpresas(conn):
	print("\t-- Mostrar Empresas --")
	cursor = conn.cursor()

	cursor.execute("SELECT * FROM empresa")	
	for row in cursor:
		print(Color.WHITE)
		print("\tID = ", row[0], "\n\tNombre = ", row[1],"\n",Color.END)

	print("-" * 40)
	cursor.close()


def mostrarPedidos(conn):
	print("\t-- Mostrar Pedidos --")
	cursor = conn.cursor()

	cursor.execute("SELECT * FROM pedido")	
	for row in cursor:
		print(Color.WHITE)
		print("\tID = ", row[0], "\n\tNombre = ", row[1], "\n\tID Cliente = ", row[2], "\n\tID Empresa = ", row[3], "\n",Color.END)

	print("-" * 40)
	cursor.close()


def LeftJoin_example(conn):
	print("\t-- Ejemplo Left Join --")
	cursor = conn.cursor()

	cursor.execute("SELECT p.nombre, e.nombre FROM pedido p LEFT JOIN empresa e ON p.empresaID = e.empresaID")
	for row in cursor:
		print(Color.WHITE)
		print("\tPedido = ", row[0], "\n\tEmpresa = ", row[1], "\n",Color.END)

	print("-" * 40)
	cursor.close()


def RightJoin_example(conn):
	print("\t-- Ejemplo Right Join --")
	cursor = conn.cursor()

	cursor.execute("SELECT p.nombre, e.nombre FROM pedido p RIGHT JOIN empresa e ON p.empresaID = e.empresaID")
	for row in cursor:
		print(Color.WHITE)
		print("\tPedido = ", row[0], "\n\tEmpresa = ", row[1], "\n",Color.END)

	print("-" * 40)
	cursor.close()


def Right_LeftJoin(conn):
	print("\t-- Ejemplo doble join (left y right) --")
	cursor = conn.cursor()

	cursor.execute("SELECT c.nombre, e.nombre, p.nombre FROM pedido p RIGHT JOIN empresa e ON p.empresaID = e.empresaID LEFT JOIN cliente c ON p.clienteID = c.clienteID")
	for row in cursor:
		print(Color.WHITE)
		print("\tCliente = ", row[0], "\n\tEmpresa = ", row[1], "\n\tPedido = ", row[2], "\n",Color.END)

	print("-" * 40)
	cursor.close()


def Right_RightJoin(conn):
	print("\t-- Ejemplo doble join (doble right) --")
	cursor = conn.cursor()

	cursor.execute("SELECT c.nombre, e.nombre, p.nombre FROM pedido p RIGHT JOIN empresa e ON p.empresaID = e.empresaID RIGHT JOIN cliente c ON p.clienteID = c.clienteID")
	for row in cursor:
		print(Color.WHITE)
		print("\tCliente = ", row[0], "\n\tEmpresa = ", row[1], "\n\tPedido = ", row[2], "\n",Color.END)

	print("-" * 40)
	cursor.close()

def full_outer_join(conn):
	print("\t-- Full Outer Join (simulado) --")
	cursor = conn.cursor()

	cursor.execute("SELECT c.nombre, e.nombre, p.nombre FROM pedido p RIGHT JOIN empresa e ON p.empresaID = e.empresaID LEFT JOIN cliente c ON p.clienteID = c.clienteID UNION SELECT c.nombre, e.nombre, p.nombre FROM pedido p RIGHT JOIN empresa e ON p.empresaID = e.empresaID RIGHT JOIN cliente c ON p.clienteID = c.clienteID")
	for row in cursor:
		print(Color.WHITE)
		print("\tCliente = ", row[0], "\n\tEmpresa = ", row[1], "\n\tPedido = ", row[2], "\n",Color.END)

	print("-" * 40)
	cursor.close()


# MAIN
conn = ConectarDB() 	# Creamos una conexion a nuestra base de datos
crearDatabase(conn)		# Creamos la base de datos
crearTabla(conn)		# Creamos las tablas

#insertarCliente(conn)
#insertarEmpresa(conn)
#insertarPedido(conn)

mostrarClientes(conn)
mostrarEmpresas(conn)
mostrarPedidos(conn)

LeftJoin_example(conn)
RightJoin_example(conn)
Right_LeftJoin(conn)
Right_RightJoin(conn)
full_outer_join(conn)

DesconectarDB(conn)		# Cerramos la conexion a la BBDD utilizada por el programa