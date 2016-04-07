

import os
from reportlab.platypus import Paragraph
from reportlab.platypus import Image
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Spacer
from reportlab.platypus import Table

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

import sqlite3 as dbapi

bbdd = dbapi.connect("BASEALUMNOs")
cursor = bbdd.cursor()

cursor.execute("select * from alumnos")
taboaBaseDatos = []

for fila in cursor:
    taboaBaseDatos.append(fila)

taboa = Table(taboaBaseDatos)

guion = []
guion.append(taboa)

documento = SimpleDocTemplate("InformeBD.pdf", pagesize=A4, showBoundary=0)
documento.build(guion)
cursor.close()
bbdd.close()