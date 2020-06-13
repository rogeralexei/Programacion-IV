import os
from pymongo import MongoClient
#----------------------------------SETUP DB------------------------------------

client= MongoClient("mongodb+srv://roger:"+os.environ["dbpass"]+"@cluster0-pmgbq.mongodb.net/slangs?retryWrites=true&w=majority")
db= client.slangs #Conect to db
slangs_collection=db.slangs #Connect to collection

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
            print(add(slangs_collection))
        elif opcion==2:
            slang=input("Inserte el slang que desea editar: ")
            valor=edit(slang.strip(),slangs_collection)
            print(valor)
        elif opcion==3:
            slang=input("Inserte el slang que desea eliminar: ")
            valor=delete(slang.strip(),slangs_collection)
            print(valor)
        elif opcion==4:
            slangs=display(slangs_collection)
        elif opcion==5:
            slang=input("Inserte el slang del cual desea buscar su definicion: ")
            definicion=get_def(slang.strip(), slangs_collection)
            print(definicion)
            
    print("Gracias por usar el programa!")

#---------------------Funciones de manipulacion--------------------------

def add(collection):
    """
    Añade una palabra con su respectiva definicion
    """
    while True:
        slang=input("Escriba la palabra que desea agregar: ")
        if collection.find_one({"slang":slang}):
            print("El slang seleccionado ya se encuentra en la base de datos")
        else:
            try:
                definition=input("Escriba la definicion de la palabra: ")
                word={"slang": slang, "definition": definition}
            except:
                print("Parece ser que hubo un problema con tu palabra")
            else:
                print("En panama "+ word["slang"]+ " significa "+ word["definition"])
                break
    result=collection.insert_one(word)
    return "Slang añadido a la base de datos con id: " + str(result.inserted_id)

def edit(slang,collection):
    """
    Edita la descripcion de una palabra
    """
    if collection.find_one({"slang": slang}):
        definition=input(f"Porfavor inserte una nueva definicion para {slang}: ")
        word=collection.find_one_and_update({"slang":slang},{"$set":{"definition": definition}})
    else:
        return "El slang seleccionado no se encuentra en la base de datos."
    word=collection.find_one({"slang":slang})
    return "Slang con id: "+str(word["_id"])+ ". Fue Editado con exito."

def delete(slang,collection):
    """
    Elimina el slang y su significado
    """
    if collection.find_one({"slang": slang}):
        try:
            collection.delete_one({"slang":slang})
        except:
            return "Ha ocurrido un error"
        else:
            return "Palabra eliminada con exito."
    else:
        return "El slang no se encuentra en la base de datos."

def display(collection):
    """
    Muestra el todas las palabras en la base de datos con su definición
    """
    try:
        words=collection.find({})
    except:
        return "Hubo un problema con la base de datos"
    else:
        print("Slangs en la base de Datos: \n")
    for word in words:
        print("-"*50)
        print("En panama " + word["slang"] + " significa "+ word["definition"])
        print("-"*50)

def get_def(slang,collection):
    """
    Muestra la definicion de la palabra seleccionada
    """
    try:
        result=collection.find_one({"slang":slang})
    except:
        return "La palabra no se encuentra en la base de datos"
    return f"\nLa definicion de {slang} es {result['definition']}"
