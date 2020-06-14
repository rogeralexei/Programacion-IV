import os
import redis as rd

#----------------------------------SETUP DB------------------------------------

r=rd.Redis("localhost", decode_responses=True)

#El path para el dump (No es obligatorio)
r.config_set("dir",os.path.dirname(os.path.abspath(__file__)))

#Usare hashes para hacerlo mas complejo. Por defecto todos 
#los valores retornados cuando se solicita una llave en un hash en redis son bytes. El decode_response =True
#nos permite hacer el decode automaticamente.

#---------------------------------Flow Control---------------------------------

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
            print(add())
        elif opcion==2:
            slang=input("Inserte el slang que desea editar: ")
            valor=edit(slang.strip())
            print(valor)
        elif opcion==3:
            slang=input("Inserte el slang que desea eliminar: ")
            valor=delete(slang.strip())
            print(valor)
        elif opcion==4:
            display()
        elif opcion==5:
            slang=input("Inserte el slang del cual desea buscar su definicion: ")
            definicion=get_def(slang.strip())
            print(definicion)
    print("Gracias por usar el programa!")
    #Un dump file se guardara automaticamente. Es simplemente para tener el dump de la interaccion , pero esta linea
    #de codigo puede ser omitida ya que Redis funciona "In memory"
    r.bgsave()

#---------------------Funciones de manipulacion--------------------------

def add():
    """
    Añade una palabra con su respectiva definicion
    """
    while True:
        slang=input("Escriba la palabra que desea agregar: ")
        definicion=input("Escriba la definicion de la palabra: ")
        try:
            r.hset("slangs",slang,definicion)
        except Exception as e:
            print(e)
        else:
            print("Palabra añadida con exito a la base de datos")
            break
    return f"{slang} significa {definicion}"

def edit(slang):
    """
    Edita la descripcion de una palabra
    """
    if r.hget("slangs",slang):
        definicion=input("Escriba la nueva definicion del Slang seleccionado ")
        try:
            r.hset("slangs",slang,definicion)
        except Exception as e:
            return e
        else:
            return "Palabra actualizada con exito en la base de datos"
    else:
        return "La palabra no se encuentra en la base de datos."
    

def delete(slang):
    """
    Elimina el slang y su significado
    """
    if r.hget("slangs",slang):
        try:
            r.hdel("slangs",slang)
        except Exception as e:
            return e
        else:
            return "Palabra eliminada exitosamente"
    else:
        return "La palabra no se encuentra en la base de datos."

def display():
    """
    Muestra el todas las palabras en la base de datos con su definición
    """
    try:
        words=r.hkeys("slangs")
        values=r.hvals("slangs")
    except Exception as e:
        return (e)
    else:
        for key,value in zip(words,values):
            print("-"*50)
            print(f"La definicion de {key} es {value}")
            print("-"*50)

def get_def(slang):
    """
    Muestra la definicion de la palabra seleccionada
    """
    if r.hget("slangs",slang):
        try:
            definicion=r.hget("slangs", slang)
        except Exception as e:
            return e
        else:
            return f"La definicion de {slang} es {definicion}"
    else:
        return f"La palabra {slang} no se encuentra en la base de datos"

