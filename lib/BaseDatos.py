# -*- coding: utf-8 -*-

import sqlite3

class BaseDatos:
    #Establecemos conexion e engadimos un cursor que percorrerá os valores
    def __init__(self):
        self.conec = sqlite3.connect("basedatos.bd")
        self.c = self.conec.cursor()

    def borrarTablaAlumnos(self): #Borrase a table, (este metodo irá comentado por si fai falta nalgun momento)
        self.c.execute("DROP TABLE alumnos")

    def crearTablaAlumnos(self): #Creamos a tabla alumnos
        self.c.execute("create table alumnos (id text primary key not null, nome text, apelido1 text, apelido2 text, telefono integer, horario text, observacion text)")
        self.conec.commit()

    def insertarAlumno(self, array): #Insertamos alumno
        consulta = "INSERT INTO alumnos VALUES (?, ?, ?, ?, ?, ?, ?)"
        self.c.execute(consulta, (array[3], array[0], array[1], array[2], array[4], array[5], array[6]))
        self.conec.commit()

    def borrarAlumno(self, id): # Eliminamos alumno
        vid = "'"+ id + "'"
        consulta = "DELETE FROM alumnos WHERE id=" + vid
        self.c.execute(consulta)
        self.conec.commit()

    def modificarDatosAlumno(self, id, array): # Editamos alumno
        consulta = "UPDATE alumnos SET nome=(?), apelido1=(?), apelido2=(?), telefono=(?), horario=(?), observacion=(?) where id=(?)"
        self.c.execute(consulta, (array[0], array[1], array[2], array[3], array[4], array[5], id))
        self.conec.commit()

    def buscarAlumno(self, id): #Buscamos un alumno segundo o seu ID
        vid = "'"+ id + "'"
        consulta = "SELECT * FROM alumnos WHERE id =" + vid
        self.c.execute(consulta)
        return list(self.c)


    def verAlumnos(self): # Método de actualizacion da taboa alumnos
        consulta = "SELECT * FROM alumnos"
        self.c.execute(consulta);
        return list(self.c)

    def coincidenciaClave(self, id): #Restriccion de coincidencia de claves
        vid = "'"+ id + "'"
        resultado = 0
        consulta = "SELECT * FROM alumnos WHERE id = " + vid
        self.c.execute(consulta)
        for i in self.c:
            resultado += 1

        return resultado



