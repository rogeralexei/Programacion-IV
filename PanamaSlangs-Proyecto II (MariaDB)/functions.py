import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql

#---------------------App db Creation-----------------------------------

app=Flask(__name__)

# Set MariaDB (Puedes cambiar las enviroment variables por tu usuario y tu contraseña, funciona con MySQL y mariadb)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://"+ os.environ["dbuser"]+":"+os.environ["dbpass"]+ "@localhost/slangs"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

db=SQLAlchemy(app)

class Slang(db.Model):
    __tablename__="slangs"

    id=db.Column(db.Integer, primary_key=True)
    palabra=db.Column(db.String(40))
    definition=db.Column(db.String(100))

    def __init__(self, palabra, definition):
        self.palabra=palabra
        self.definition=definition

    def __repr__(self):
        return f"En panamá {self.palabra} significa {self.definition}"

db.create_all()

#---------------------Funciones base-----------------------------------

def control():
    while True:
        try:
            opc=int(input(""" \nSelecciona la opcion que desees:
            1) Añadir una palabra
            2) Editar palabra existente
            3) Eliminar palabra existente
            4) Ver Listado de palabras
            5) Buscar el significado de una palabra
            6) Salir
            """))
        except:
            print("Valor no valido")
        else:
            if opc in range(1,6):
                return opc
            elif opc==6:
                return None
            else:
                print("Valor no valido")

def main(opcion=True):
    print("Bienvenido al programa de slangs panameños")
    while opcion:
        opcion=control()
        if opcion==1:
            add()
        elif opcion==2:
            slang=input("Inserte el slang que desea editar: ")
            edit(slang.strip())
        elif opcion==3:
            slang=input("Inserte el slang que desea eliminar: ")
            valor=delete(slang.strip())
            if valor:
                print(valor)
        elif opcion==4:
            display()
        elif opcion==5:
            slang=input("Inserte el slang del cual desea buscar su definicion: ")
            get_def(slang)
    print("Gracias por usar el programa!")

# #---------------------Funciones de manipulacion--------------------------

def add():
    """
    Añade una palabra con su respectiva definicion
    """
    while True:
        slang=input("Escriba la palabra que desea agregar: ")
        definition=input("Escriba la definicion de la palabra: ")
        try:
            slang=Slang(slang.strip(), definition.strip())
        except:
            print("Parece ser que hubo un problema con tu palabra")
        else:
            print(slang)
            db.session.add(slang)
            db.session.commit()
            break

def edit(slang):
    """
    Edita la descripcion de una palabra
    """
    word=Slang.query.filter_by(palabra=slang).first()
    try:
        word.definition=input("Ingrese la nueva definicion: ")
    except:
        print("Slang no disponible")
        return None
    db.session.commit()

def delete(slang):
    """
    Elimina el slang y su significado
    """
    word=Slang.query.filter_by(palabra=slang).first()
    try:
        db.session.delete(word)
    except:
        print("El slang no esta en la base de datos")
        return None
    db.session.commit()


def display():
    """
    Muestra el todas las palabras en la base de datos con su definición
    """
    words=Slang.query.all()
    if words:
        for word in words:
            print("-"*50)
            print(word)
            print("-"*50)
    else:
        return None

def get_def(slang):
    """
    Muestra la definicion de la palabra seleccionada
    """
    words=Slang.query.filter_by(palabra=slang)
    print(f"{slang} significa: ")
    for i,word in enumerate(words):
        print(str(i+1)+ ". " + word.definition)
        
