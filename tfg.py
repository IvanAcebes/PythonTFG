#!/usr/bin/python
#encoding: utf-8

def ListUser():
	
	print("")
	print("Lista de usuarios")
	print("---------------------")
	bases = "select user from mysql.user"
	cursor.execute(bases)
	filas = cursor.fetchall()
	for fila in filas:
		print(*fila, end='\n')
		print("")
	print("---------------------")
	print("")

def ListBD():
	
	print("")
	print("Bases de Datos:")
	print("---------------------")
	print("")
	bases = "show databases;"
	cursor.execute(bases)
	filas = cursor.fetchall()
	for fila in filas:
		print(*fila, end='\n')
		print("")
	print("---------------------")
	print("")

def ListTabla(x):
	
	print("")
	print("Tablas de la Base de Datos " +x +":")
	print("---------------------")
	print("")
	bases = "show tables;"
	cursor.execute(bases)
	filas = cursor.fetchall()
	for fila in filas:
		print(*fila, end='\n')
		print("")
	print("---------------------")
	print("")


def CompUser(x):
	
	bases = "select * from mysql.user where user='" +x +"'"
	cursor.execute(bases)
	filas = cursor.fetchall()

	if not filas:
		print("")
		input("El usuario " +x +" no existe.")
		return 1
	else:
		print()

def CompBD(x):
	
	try:
		bases = "use " +x +""
		cursor.execute(bases)
	except:
		print("")
		input("La Base de Datos " +x +" no existe.")
		return 1

def CompTabla(x, y):
	
	try:
		bases = "select * from " +x + "." +y
		cursor.execute(bases)
		
	except:
		print("")
		input("La tabla " +y +" no existe en la base de datos " +x)
		return 1


def GestionUser():
    while True:
        
        from subprocess import call
        call('clear')

        print("-------------------------------------------------------")
        print("")
        print("[1] Crear nuevo usuario")
        print("")
        print("[2] Borrar usuario")
        print("")
        print("[3] Ver permisos de usuarios")
        print("")
        print("[4] Permisos avanzados")
        print("")
        print("[5] Volver")
        print("")
        print("-------------------------------------------------------")
        print("")
 
        numUs = input("Seleccione el número de la opción que desea realizar: ")

        if numUs == "1":
            print("")
            NewUs = input("Intruza el nombre del nuevo usuario (C|c para cancelar): ")
            if NewUs == "c" or NewUs == "C":
                continue
            print("")

            errorNom = CompUser(NewUs)
            if errorNom == 1:
                print("")
            else:
                input("El usuario " +NewUs +" ya existe.")
                continue

            PassUs = input("Intruza la contraseña para el nuevo usuario " +NewUs +" (C|c para cancelar): ")
            if PassUs == "c" or PassUs == "C":
                continue
            
            try:
                bases = "create user '" +NewUs +"'@'localhost' identified by '" +PassUs +"'"
                cursor.execute(bases)
            except pymysql.err.OperationalError:
                print("")
                input("Error. La contraseña no es segura.")
                continue
            except:
                print("")
                input("Ha ocurrido un error al crear el nuevo usuario.")
                continue

            ListUser()

            print("")
            input("Pulse intro para continuar: ")

        elif numUs == "2":

            ListUser()

            DelUs = input("Intruza el nombre del usuario que desea borrar (C|c para cancelar): ")

            if DelUs == "c" or DelUs == "C":
                continue
            print("")

            errorNom = CompUser(DelUs)
            if errorNom == 1:
                continue
            else:
                print()

            SN = input("¿Seguro que desea borrar para siempre el usuario " +DelUs +"? (S o N): ")

            if SN == "n" or SN == "N":
                print("")
                input("No se ha borrado el usuario " +DelUs +". Pulse intro para continuar: ")
                continue
            elif SN == "s" or SN == "S":
                print("")
            else:
                print("")
                input("Opción Incorrecta, se esperaba (S o N). Pulse intro para continuar: ")
                continue
            try:
                bases = "drop user '" +DelUs +"'@'localhost'"
                cursor.execute(bases)
            except:
                print("")
                input("Ha ocurrido un error al borrar el usuario.")
                continue

            ListUser()

            print("")
            input("Pulse intro para continuar: ")

        elif numUs == "3":
            
            ListUser()

            NombreUs = input("Intruza el nombre del usuario (C|c para cancelar): ")
            if NombreUs == "c" or NombreUs == "C":
                continue

            errorNom = CompUser(NombreUs)
            if errorNom == 1:
                continue
            else:
                print()

            bases = "select column_name from information_schema.columns where table_name = 'user';"
            cursor.execute(bases)
            resultado = cursor.fetchall()
                
            print('\n')

            x = -1

            for y in range(len(resultado)):

                h = str(*resultado[x+1])

                print(*resultado[(x + 1)], sep='\n', end=" ----- " )

                bases = "select " +h +" from mysql.user where user='"+NombreUs +"'"
                cursor.execute(bases)
                filas = cursor.fetchall()

                print(*filas, end='\n' )
            
                x = x+1
    

            print("")
            input("Pulse intro para continuar: ")
 
        elif numUs == "4":

            ListUser()

            PermUs = input("Intruduzca el usuario al que gestionar(C|c para cancelar): ")
            if PermUs == "c" or PermUs == "C":
                continue
            print("")

            errorNom = CompUser(PermUs)
            if errorNom == 1:
                continue
            else:
                print()

            print("---------------------")
            print("")
            print("Grant (Añade permisos)")
            print("")
            print("Revoke (Elimina permisos)")
            print("")
            print("---------------------")
            
            print("")
            GRUs = input("Introduzca una opción (C|c para cancelar): ")
            if GRUs == "c" or GRUs == "C":
                continue

            if GRUs == "Grant" or GRUs == "grant" or GRUs == "GRANT":
                ToFrom = "to"
            elif GRUs == "Revoke" or GRUs == "revoke" or GRUs == "REVOKE":
                ToFrom = "from"
            else:
                print("")
                input("Error, se debe seleccionar Grant o Revoke. Pulse intro para continuar.")
                continue


            print("-------------------------------------------------------")
            print("")
            print("Create (Permite crear nuevas tablas o bases de datos.)")
            print("")
            print("Drop (Permite eliminar tablas o bases de datos.)")
            print("")
            print("Delete (Permite eliminar registros de tablas.)")
            print("")
            print("Insert (Permite insertar registros de tablas.)")
            print("")
            print("Select (Permite leer registros de tablas.)")
            print("")
            print("Update (Permite actualizar perisos de tablas.)")
            print("")
            print("Show Databases (Permite listar las bases de datos existentes.)")
            print("")
            print("All privileges (Permite usar todos los otros permisos.)")
            print("")
            print("-------------------------------------------------------")

            print("")
            PerUs = input("Introduzca un permiso o varios separados por comas (, ) (C|c para cancelar): ")
            if PerUs == "c" or PerUs == "C":
                continue

            bases = GRUs +" " +PerUs +" on *.* " +ToFrom +" '" +PermUs +"'@'localhost'"
            
            try:
                cursor.execute(bases)
            except pymysql.err.ProgrammingError:
                print("")
                input("Los permisos indicados no son correctos")
                continue

            bases = "select column_name from information_schema.columns where table_name = 'user';"
            cursor.execute(bases)
            resultado = cursor.fetchall()
        
            print("")
            print("----------------------")
            print("Permisos del usuario" +PermUs)
            print("----------------------")
            print("")

            x = -1
            for y in range(len(resultado)):

                h = str(*resultado[x+1])

                print(*resultado[(x + 1)], sep='\n', end=" ----- " )

                bases = "select " +h +" from mysql.user where user='"+PermUs +"'"
                cursor.execute(bases)
                filas = cursor.fetchall()

                print(*filas, end='\n' )
                
                x = x+1
            
            print("")
            input("Pulse intro para continuar: ")

        elif numUs == "5": 
           return 1
        
        else:
            print("")
            input("Opción Incorrecta, debe ser un número entre el 1 y el 5.")
            continue

def GestionBD():
    while True:

        from subprocess import call
        call('clear')

        print("-------------------------------------------------------")
        print("")
        print("[1] Ver Bases de datos")
        print("")
        print("[2] Ver una tabla completa")
        print("")
        print("[3] Borrar un tabla")
        print("")
        print("[4] Sentencias avanzadas")
        print("")
        print("[5] Volver")
        print("")
        print("-------------------------------------------------------")
        print("")
 
        numSQL = input("Seleccione el número de la opción que desea realizar: ")
 
        if numSQL == "1":
            ListBD()
            
            input("Pulse intro parea continuar: ")
 
        elif numSQL == "2":

            ListBD()

            NombreBD = input("Intruza la Base de Datos donde se encuentra la tabla (C|c para cancelar): ")
            if NombreBD == "c" or NombreBD == "C":
                continue

            errorBD = CompBD(NombreBD)
            if errorBD == 1:
                continue
            else:
                print()
            
            ListTabla(NombreBD)

            NombreTabla = input("Intruza el nombre de la tabla que desea ver (C|c para cancelar): ")
            if NombreTabla == "c" or NombreBD == "C":
                continue
            
            errorTabla = CompTabla(NombreBD, NombreTabla)

            if errorTabla == 1:
                continue
            else:
                print()

            bases = "select group_concat(column_name) from information_schema.columns where table_schema = '" +NombreBD +"' and table_name = '" +NombreTabla +"'"
            cursor.execute(bases)
            resultado = cursor.fetchall()
            for fila in resultado:
                print("")
                print("---------------------")
                print(*fila, sep=" ,", end='\n' )
                print("---------------------")

            bases = "select * from " +NombreTabla
            cursor.execute(bases)
            resultado = cursor.fetchall()
            for fila in resultado:
                print(*fila, sep=", ", end='\n' )
                print("---------------------")
                
            print("")
            input("Pulse intro parea continuar: ")
 
        elif numSQL == "3":

            ListBD()

            NombreBD = input("Intruza la Base de Datos donde se encuentra la tabla (C|c para cancelar): ")
            if NombreBD == "c" or NombreBD == "C":
                continue

            errorBD = CompBD(NombreBD)
            if errorBD == 1:
                continue
            else:
                print()

            ListTabla(NombreBD)

            NombreTabla = input("Intruza el nombre de la tabla que desea borrar (C|c para cancelar): ")
            if NombreTabla == "c" or NombreTabla == "C":
                continue
            print("")

            errorTabla = CompTabla(NombreBD, NombreTabla)

            if errorTabla == 1:
                continue
            else:
                print()

            SN = input("¿Seguro que desea borrar para siempre la tabla " +NombreTabla +"? (S o N): ")

            if SN == "n" or SN == "N":
                print("")
                input("No se ha borrado la tabla " +NombreTabla +". Pulse intro para continuar: ")
                continue
            elif SN == "s" or SN == "S":
                print("")
            else:
                print("")
                input("Opción Incorrecta, se esperaba (S o N). Pulse intro para continuar: ")
                continue

            bases = "drop table if exists " +NombreTabla
            cursor.execute(bases)

            ListTabla(NombreBD)

            print("")
            input("Pulse intro para continuar: ")
 
        elif numSQL == "4":
            print("")
            SentSQL = input("Intruduzca la sentencia SQL que desea utilizar (C|c para cancelar): ")
            if SentSQL == "c" or SentSQL == "C":
                continue

            try:
                bases = SentSQL
                cursor.execute(bases)
                filas = cursor.fetchall()
            except:
                print("")
                input("Error al ejecutar la sentencia SQL.")
                continue

            print("")
            for fila in filas:
                print(*fila, end='\n')
        
            print("")
            input("Pulse intro para continuar: ")
        
        elif numSQL == "5": 
           return 1
 
        else:
            print("")
            input("Opción Incorrecta, debe ser un número entre el 1 y el 5.")
            continue

def ElegirOpcion():
    while True:
        from subprocess import call
        call('clear')

        print("-------------------------------------------------------")
        print("")
        print("                 Eres el usuario " + usuario)
        print("")
        print("-------------------------------------------------------")
        print("")
        print("[1] Gestionar usuarios")
        print("")
        print("[2] Gestionar Bases de Datos")
        print("")
        print("[3] Cambiar usuario")
        print("")
        print("[4] Salir del programa")
        print("")
        print("-------------------------------------------------------")
        print("")
 
        numOp = input("Seleccione el número de la opción que desea realizar: ")
    
        if numOp == "1":
            GestionUser()
            if GestionUser == 1:
                continue
            
        elif numOp == "2":
            GestionBD()
            if GestionBD == 1:
                continue

        elif numOp == "3":
                return 1
        
        elif numOp == "4":
            cursor.close()
            conexion.commit()
            conexion.close()

            print("")
            print("Gracias por usar nuestro gestor de Bases de Datos")
            print("")

            import sys
            sys.exit(101)
 
        else:
            print("")
            input("Opción Incorrecta, debe ser un número entre el 1 y el 4.")
            continue
   

while True:
    from subprocess import call
    call('clear')
 
    print("-------------------------------------------------------")
    print("")
    print("Bienvenido al programa gestor de bases de datos")
    print("")
    print("-------------------------------------------------------")
    print("")

    usuario = input("Introduzca el usuario con el que desea trabajar: ")
    print("")
    password = input("introduzca su contraseña: ")

    try:
        import pymysql
        conexion = pymysql.connect(
        host="localhost", 
        user=usuario, 
        passwd=password,  
        )
        cursor = conexion.cursor()
    except:
        print("")
        input("El usuario selecionado no ha podido iniciar sesión.")
        continue
    
    ElegirOpcion()
    if ElegirOpcion == 1:
            continue
