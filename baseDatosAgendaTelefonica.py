import sqlite3 as dbapi #para imprimir los datos del SQLite

agendaTelf= (("Juan", "Pérez", "605 568 478"),
             ("Ana", "Sánchez", "986 120 967"),
             ("José", "López", "689 552 123"),
             ("Manuel", "García", "602 405 633")) # Datos de la agenda telefónica

bbdd= dbapi.connect("bdListinTelefonico.dat")
c = bbdd.cursor()

try:
    c.execute("""create table listaTelefonos (nombre text, apellido text, telefono text)""")
except dbapi.DatabaseError as e:
    print ("Error creando tabla listaTelefonos: " + e)

try:
    for datos in agendaTelf:
        c.execute("""insert into listaTelefonos values(?,?,?)""",datos)

    bbdd.commit()
except dbapi.DatabaseError as e:
    print ("Error insertando en la tabla listaTelefonos: " + e)

c.close()
bbdd.close()