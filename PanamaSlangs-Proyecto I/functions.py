import sqlite3
from classes import Slang

conn=sqlite3.connect("slang.db")

c=conn.cursor()

#Quitar el comentario en caso de desear modificar la tabla o crearla si la DB no cuenta con ella

# c.execute("""CREATE TABLE slangs (
#             slang text,
#             definition text
#             )""") 

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
            valor=edit(slang.strip())
            if not valor:
                print("La palabra no se encuentra en la base de datos")
            else:
                print(valor)
        elif opcion==3:
            slang=input("Inserte el slang que desea eliminar: ")
            valor=delete(slang.strip())
            if valor:
                print(valor)
        elif opcion==4:
            slangs=display()
            if slangs:
                for slang,definicion in slangs:
                    print("-"*50)
                    print(f"En Panama {slang} significa {definicion}")
                    print("-"*50)
        elif opcion==5:
            slang=input("Inserte el slang del cual desea buscar su definicion: ")
            definiciones=get_def(slang)
            if definiciones:
                for definicion in definiciones:
                    print(f"\n{slang} significa {definicion[0]}")
            else:
                print("La palabra seleccionada no esta en la base de datos.")
    print("Gracias por usar el programa!")

#---------------------Funciones de manipulacion--------------------------

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
            break
    with conn:
        c.execute("INSERT INTO slangs VALUES (:slang,:definition)", {"slang":slang.slang, "definition": slang.definition}) 
        print("Slang añadido a la base de datos")
        return slang

def edit(slang):
    """
    Edita la descripcion de una palabra
    """
    c.execute("SELECT definition FROM slangs WHERE slang=:slang",{"slang":slang})
    if not c.fetchone():
        print("El Slang solicitado no existe en la base de datos.")
        return None
    definition=input("Cual sera la nueva definicion de la palabra {}: ".format(slang))
    with conn:
        try:
            c.execute("UPDATE slangs SET definition= :definition WHERE slang=:slang", {"definition":definition, "slang":slang})
        except:
            print("Hubo un problema en la actualizacion")
            return None
    return "Definicion actualizada con exito"

def delete(slang):
    """
    Elimina el slang y su significado
    """
    c.execute("SELECT definition FROM slangs WHERE slang=:slang",{"slang":slang})
    if not c.fetchone():
        print("El Slang solicitado no existe en la base de datos.")
        return None
    with conn:
        try:
            c.execute("DELETE FROM slangs where slang=:slang", {"slang":slang})
        except:
            print("Ocurrio un problema durante la eliminacion")
        return "Palabra eliminada con exito"

def display():
    """
    Muestra el todas las palabras en la base de datos con su definición
    """
    try:
        c.execute("SELECT * FROM slangs")
    except:
        print("Ha ocurrido un problema con la base de datos")
        return None
    return c.fetchall()

def get_def(slang):
    """
    Muestra la definicion de la palabra seleccionada
    """
    try:
        c.execute("SELECT definition FROM slangs WHERE slang=:slang",{"slang":slang})
    except:
        print("Ha ocurrido un problema con la base de datos")
        return None
    return c.fetchall()

